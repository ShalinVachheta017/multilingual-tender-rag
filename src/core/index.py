# core/index.py
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Optional
import hashlib
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
import numpy as np
from tqdm import tqdm
import torch
from uuid import uuid5, NAMESPACE_URL

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from sentence_transformers import SentenceTransformer

from .chunking import PageAwareChunker
from .prepare import init_worker, prepare_pdf
from .io import PDFLoader, ExcelMetadataJoiner
from .config import CFG



class Indexer:
    """
    Build or append to a Qdrant collection for the tender RAG system.

    - fresh=True  : (re)create the collection to match current embedding dim
    - fresh=False : keep the collection; validates vector size; upserts are idempotent
    """

    def __init__(self, cfg=CFG, fresh: bool = True):
        self.cfg = cfg
        self.fresh = bool(fresh)

        # ---- device selection ----
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.device == "cuda":
            try:
                name = torch.cuda.get_device_name(0)
                mem = torch.cuda.get_device_properties(0).total_memory // (1024**3)
                tqdm.write(f"Using GPU: {name}  ({mem} GB)")
                torch.set_float32_matmul_precision("high")
            except Exception:
                tqdm.write("Using GPU")
        else:
            tqdm.write(" Using CPU - GPU not available")

        # ---- embedder (model, revision and remote-code switch come from CFG) ----
        self.embedder = SentenceTransformer(
            model_name_or_path=cfg.embed_model,
            revision=cfg.embed_revision,
            trust_remote_code=cfg.embed_trust_remote_code,
            device=self.device,
        )
        self.raw_dim = self._get_embed_dim(self.embedder)
        # Effective dim = min(configured, raw). Keeps compatibility if model grows.
        self.effective_dim = min(int(getattr(cfg, "embed_dim", self.raw_dim)), self.raw_dim)

        # ---- qdrant client ----
        self.client = QdrantClient(url=cfg.qdrant_url, prefer_grpc=False)

        # ---- collection bootstrap/validate ----
        self._ensure_collection(self.effective_dim)

        # ---- helpers ----
        self.loader = PDFLoader()  # swap to OCR mode in build_ocr_only()
        self.chunker = PageAwareChunker(cfg.chunk_size, cfg.chunk_overlap)
        self.joiner = ExcelMetadataJoiner()

        # ---- text put in front of every chunk (empty for BGE-M3, "search_document: " for Jina) ----
        self.doc_prefix = cfg.embed_doc_prefix

    # ---------------- helpers ----------------

    def _get_embed_dim(self, model: SentenceTransformer) -> int:
        try:
            return int(model.get_sentence_embedding_dimension())
        except Exception:
            v = model.encode("probe", normalize_embeddings=True)
            return int(len(v))

    def _existing_collection_dim(self) -> Optional[int]:
        try:
            info = self.client.get_collection(self.cfg.qdrant_collection)
            vecs = info.config.params.vectors
            if hasattr(vecs, "size"):  # single vector
                return int(vecs.size)
            # named vectors: pick first
            for _, vp in vecs.items():
                return int(vp.size)
        except Exception:
            return None
        return None

    def _create_collection(self, dim: int) -> None:
        self.client.create_collection(
            collection_name=self.cfg.qdrant_collection,
            vectors_config=qmodels.VectorParams(size=dim, distance=qmodels.Distance.COSINE),
            hnsw_config=qmodels.HnswConfigDiff(m=16, ef_construct=64),
            optimizers_config=qmodels.OptimizersConfigDiff(indexing_threshold=20_000),
            on_disk_payload=False,
        )
        tqdm.write(f"Created collection: {self.cfg.qdrant_collection} (dim={dim})")

    def _ensure_collection(self, dim: int) -> None:
        existing_dim = self._existing_collection_dim()
        if existing_dim is None:
            if self.fresh:
                # Clean safety in case a partial/corrupted collection exists
                try:
                    self.client.delete_collection(self.cfg.qdrant_collection)
                except Exception:
                    pass
            self._create_collection(dim)
            return

        # Collection exists
        if self.fresh:
            try:
                self.client.delete_collection(self.cfg.qdrant_collection)
                tqdm.write(f" Deleted old collection: {self.cfg.qdrant_collection}")
            except Exception as e:
                tqdm.write(f" Could not delete existing collection (continuing): {e}")
            self._create_collection(dim)
            return

        # Append mode: validate dims
        if existing_dim != dim:
            raise RuntimeError(
                f"Qdrant collection dim ({existing_dim}) != effective embed dim ({dim}). "
                f"Either recreate with --mode fresh or set CFG.embed_dim={existing_dim} "
                f"(current model raw_dim={self.raw_dim})."
            )

    def _embed(self, texts: List[str]) -> np.ndarray:
        """
        Embed texts with:
          - Jina document prefix (from CFG)
          - autocast on CUDA
          - Matryoshka crop to self.effective_dim
        """
        if not texts:
            return np.zeros((0, self.effective_dim), dtype="float32")

        prefixed = [self.doc_prefix + (t or "") for t in texts]

        if self.device == "cuda":
            torch.cuda.empty_cache()
            with torch.inference_mode(), torch.cuda.amp.autocast():
                out = self.embedder.encode(
                    prefixed,
                    batch_size=self.cfg.embed_batch_size,
                    normalize_embeddings=True,
                    convert_to_numpy=True,
                    show_progress_bar=False,
                )
        else:
            with torch.inference_mode():
                out = self.embedder.encode(
                    prefixed,
                    batch_size=self.cfg.embed_batch_size,
                    normalize_embeddings=True,
                    convert_to_numpy=True,
                    show_progress_bar=False,
                )

        out = np.asarray(out, dtype="float32")
        if out.shape[1] > self.effective_dim:
            orig = out.shape[1]
            out = out[:, : self.effective_dim]
            tqdm.write(f"Cropped embeddings {orig} {self.effective_dim} dims")

        if self.device == "cuda":
            torch.cuda.empty_cache()
        return out

    def _point_id(self, doc_hash: str, chunk_idx: int) -> str:
        """Deterministic UUID for points (idempotent upserts)."""
        return str(uuid5(NAMESPACE_URL, f"{doc_hash}|{chunk_idx}"))

    @staticmethod
    def _tender_id(pdf: Path, base: Path) -> str:
        """The first folder under the extract dir is the tender id (see ZipIngestor)."""
        parts = pdf.relative_to(base).parts
        return parts[0] if len(parts) > 1 else ""

    @staticmethod
    def _list_pdfs(base: Path, tenders: Optional[List[str]]) -> List[Path]:
        roots = [base / t for t in tenders] if tenders else [base]
        return sorted(p for r in roots for p in r.rglob("*.pdf"))

    def _hash_file(self, pdf_path: Path) -> str:
        """Robust file hash (fallback to path string if read fails)."""
        try:
            return hashlib.sha1(pdf_path.read_bytes()).hexdigest()
        except Exception:
            return hashlib.sha1(str(pdf_path).encode("utf-8")).hexdigest()

    def _prepared(self, pdfs: List[Path], workers: int):
        """Yield (pdf, chunks, error) in order. Reading, OCR and chunking are the CPU part of the work.

        With workers > 1 they run in other processes, so the next PDFs are being read and OCR'd
        while the GPU embeds the current one.
        """
        size, overlap = self.cfg.chunk_size, self.cfg.chunk_overlap
        if workers <= 1:
            for pdf in pdfs:
                yield prepare_pdf(pdf, size, overlap)
            return
        with ProcessPoolExecutor(max_workers=workers, initializer=init_worker) as pool:
            yield from pool.map(prepare_pdf, pdfs, repeat(size), repeat(overlap))

    # --------------- main flows ----------------

    def build(self, extract_dir: Path | None = None, tenders: Optional[List[str]] = None, workers: int = 1):
        """
        Build (fresh or append) the index with batch upserts.
        - In fresh mode, the collection was recreated in __init__
        - In append mode, point IDs are stable and will overwrite duplicates
        """
        base = Path(extract_dir or self.cfg.extract_dir)
        pdfs = self._list_pdfs(base, tenders)
        tqdm.write(f"Found {len(pdfs)} PDFs to process in {base}")
        if not pdfs:
            tqdm.write(" No PDF files found in extract directory")
            return

        BUFFER_SIZE = int(self.cfg.embed_flush_chunks)
        points_buffer: List[qmodels.PointStruct] = []
        total_chunks = 0
        processed_files = 0

        for pdf_idx, (pdf, chunks, error) in enumerate(
                tqdm(self._prepared(pdfs, workers), total=len(pdfs), desc="PDFs", unit="file"), start=1):
            try:
                if error:
                    raise RuntimeError(error)

                if not chunks:
                    tqdm.write(f" Skipped (no text): {pdf.name}")
                    continue

                h = self._hash_file(pdf)
                tender_id = self._tender_id(pdf, base)

                # Prepare payloads and texts
                payloads: List[Dict] = []
                texts: List[str] = []
                for c in chunks:
                    meta = self.joiner.enrich(c.source_path, {**c.meta, "dtad_id": tender_id})
                    base_payload = c.payload()  # expected to include chunk_idx/page/source
                    # Normalize/augment payload to be JSON-safe & informative
                    pl = {
                        **base_payload,
                        **meta,
                        "source_path": str(base_payload.get("source_path") or c.source_path or ""),
                        "doc_hash": h,
                        "dtad_id": tender_id,
                        "rel_path": pdf.relative_to(base).as_posix(),
                        "text": (c.text or "")[:1500],  # snippet for reranker/UI
                    }
                    payloads.append(pl)
                    texts.append(c.text or "")

                # Batch over encode output for throughput (4× embed_batch_size is a good start)
                batch_size = min(len(texts), max(1, int(self.cfg.embed_batch_size) * 4))
                for i in range(0, len(texts), batch_size):
                    batch_texts = texts[i : i + batch_size]
                    batch_payloads = payloads[i : i + batch_size]

                    vecs = self._embed(batch_texts)

                    for v, pl in zip(vecs, batch_payloads):
                        cid = int(pl.get("chunk_idx", -1))
                        points_buffer.append(
                            qmodels.PointStruct(
                                id=self._point_id(pl["doc_hash"], cid),
                                vector=v.tolist(),
                                payload=pl,
                            )
                        )

                    if len(points_buffer) >= BUFFER_SIZE:
                        self.client.upsert(
                            collection_name=self.cfg.qdrant_collection,
                            points=points_buffer,
                            wait=False,
                        )
                        tqdm.write(f"Uploaded batch: {len(points_buffer)} points")
                        total_chunks += len(points_buffer)
                        points_buffer.clear()
                        if self.device == "cuda":
                            torch.cuda.empty_cache()

                processed_files += 1
                tqdm.write(f"Processed {len(chunks)} chunks from {pdf.name}")

            except Exception as e:
                tqdm.write(f"Error processing {pdf.name}: {e}")
                continue

        # Final flush
        if points_buffer:
            self.client.upsert(
                collection_name=self.cfg.qdrant_collection,
                points=points_buffer,
                wait=False,
            )
            tqdm.write(f"Final upload: {len(points_buffer)} points")
            total_chunks += len(points_buffer)

        if self.device == "cuda":
            torch.cuda.empty_cache()

        tqdm.write("Indexing complete!")
        tqdm.write(f"Processed: {processed_files}/{len(pdfs)} files")
        tqdm.write(f"Total chunks upserted: {total_chunks}")
        tqdm.write("Your German document RAG system is ready!")

    def build_ocr_only(self, extract_dir: Path | None = None, tenders: Optional[List[str]] = None):
        """
        Process only OCR-needing PDFs (does NOT recreate collection).
        Heuristic: files with no extractable text via PDFLoader(use_ocr=False)
        """
        base = Path(extract_dir or self.cfg.extract_dir)
        skipped_files: List[Path] = []
        loader_no_ocr = PDFLoader(use_ocr=False)

        for pdf in self._list_pdfs(base, tenders):
            try:
                pages = loader_no_ocr.load_pages(pdf)
                if not pages or sum(len(p.text or "") for p in pages) == 0:
                    skipped_files.append(pdf)
            except Exception:
                skipped_files.append(pdf)

        tqdm.write(f"Found {len(skipped_files)} previously skipped files for OCR processing")
        if not skipped_files:
            tqdm.write("No skipped files found! All documents already processed.")
            return

        # Enable OCR for this processing
        self.loader = PDFLoader(use_ocr=True)

        BUFFER_SIZE = int(self.cfg.embed_flush_chunks)
        points_buffer: List[qmodels.PointStruct] = []
        new_chunks_count = 0
        processed_files = 0

        for i, pdf_path in enumerate(tqdm(skipped_files, desc="OCR PDFs", unit="file"), start=1):
            try:

                pages = self.loader.load_pages(pdf_path)
                if not pages or sum(len(p.text or "") for p in pages) == 0:
                    tqdm.write(f" Still no text after OCR: {pdf_path.name}")
                    continue

                chunks = self.chunker.split(pages)
                if not chunks:
                    tqdm.write(f" No chunks created: {pdf_path.name}")
                    continue

                h = self._hash_file(pdf_path)
                tender_id = self._tender_id(pdf_path, base)

                payloads: List[Dict] = []
                texts: List[str] = []
                for c in chunks:
                    meta = self.joiner.enrich(c.source_path, {**c.meta, "dtad_id": tender_id})
                    base_payload = c.payload()
                    pl = {
                        **base_payload,
                        **meta,
                        "source_path": str(base_payload.get("source_path") or c.source_path or ""),
                        "doc_hash": h,
                        "dtad_id": tender_id,
                        "rel_path": pdf_path.relative_to(base).as_posix(),
                        "text": (c.text or "")[:1500],
                        "processed_with_ocr": True,
                    }
                    payloads.append(pl)
                    texts.append(c.text or "")

                vecs = self._embed(texts)

                for v, pl in zip(vecs, payloads):
                    cid = int(pl.get("chunk_idx", -1))
                    points_buffer.append(
                        qmodels.PointStruct(
                            id=self._point_id(pl["doc_hash"], cid),
                            vector=v.tolist(),
                            payload=pl,
                        )
                    )

                if len(points_buffer) >= BUFFER_SIZE:
                    self.client.upsert(
                        collection_name=self.cfg.qdrant_collection,
                        points=points_buffer,
                        wait=False,
                    )
                    tqdm.write(f"Uploaded OCR batch: {len(points_buffer)} points")
                    new_chunks_count += len(points_buffer)
                    points_buffer.clear()

                processed_files += 1
                if self.device == "cuda":
                    torch.cuda.empty_cache()

                tqdm.write(f"Added {len(chunks)} OCR chunks from {pdf_path.name}")

            except Exception as e:
                tqdm.write(f"Error processing {pdf_path.name}: {e}")
                continue

        # Final batch upload
        if points_buffer:
            self.client.upsert(
                collection_name=self.cfg.qdrant_collection,
                points=points_buffer,
                wait=False,
            )
            tqdm.write(f"Final OCR upload: {len(points_buffer)} points")
            new_chunks_count += len(points_buffer)

        # Basic OCR stats if PDFLoader tracks any
        if hasattr(self.loader, "get_ocr_stats"):
            ocr_stats = self.loader.get_ocr_stats()
            tqdm.write("\nOCR Processing Complete!")
            tqdm.write(f"Files processed: {processed_files}")
            tqdm.write(f"New chunks added: {new_chunks_count}")
            tqdm.write(f"OCR attempts: {ocr_stats.get('attempted', 'n/a')}")
            tqdm.write(f"OCR successful: {ocr_stats.get('successful', 'n/a')}")
            tqdm.write(f"OCR failed: {ocr_stats.get('failed', 'n/a')}")

        if new_chunks_count > 0:
            tqdm.write("Your German document RAG system now has enhanced coverage!")
