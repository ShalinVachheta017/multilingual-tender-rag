"""The CPU half of indexing: read each PDF (OCR for scanned pages), cut it into chunks, and keep the result.

One PDF becomes one plain, JSON-able record, so the result can be saved to a file once and embedded many times
(different models, different experiments) without reading or OCR-ing the PDFs again.

Lives in its own light module so worker processes can import it without loading torch.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Iterator, List, Optional

from .chunking import PageAwareChunker
from .io import PDFLoader

_loader: Optional[PDFLoader] = None


def init_worker() -> None:
    """Each worker runs Tesseract; keep Tesseract itself to one thread so workers do not fight over cores."""
    os.environ["OMP_THREAD_LIMIT"] = "1"


def prepare_record(pdf: Path, base: Path, size: int, overlap: int) -> dict:
    """Read, OCR and chunk one PDF. Never raises: a problem is reported in the record's "error" field.

    The first folder under `base` is the tender id (see ZipIngestor).
    """
    global _loader
    pdf, base = Path(pdf), Path(base)
    rel = pdf.relative_to(base)
    record = {
        "tender_id": rel.parts[0] if len(rel.parts) > 1 else "",
        "rel_path": rel.as_posix(),
        "doc_hash": "",
        "ocr_pages": 0,
        "ocr_page_numbers": [],
        "chunks": [],
        "error": None,
    }
    try:
        record["doc_hash"] = hashlib.sha1(pdf.read_bytes()).hexdigest()
        if _loader is None:
            _loader = PDFLoader()
        ocr_before = _loader.ocr_stats["attempted"]
        pages = _loader.load_pages(pdf)
        record["ocr_pages"] = _loader.ocr_stats["attempted"] - ocr_before
        record["ocr_page_numbers"] = [p.page_number for p in pages if p.meta.get("used_ocr")]
        record["chunks"] = [
            {"chunk_idx": c.chunk_index, "page_start": c.page_start, "page_end": c.page_end, "text": c.text}
            for c in PageAwareChunker(size, overlap).split(pages)
        ]
    except Exception as e:  # noqa: BLE001
        record["error"] = f"{type(e).__name__}: {e}"
    return record


def read_records(path: Path, tenders: Optional[List[str]] = None) -> Iterator[dict]:
    """Read the saved records (one JSON object per line), optionally only for some tenders."""
    with Path(path).open(encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            if not tenders or record["tender_id"] in tenders:
                yield record
