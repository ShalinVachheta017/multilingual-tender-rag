"""Step 2 of 3: build the Qdrant index from the PDFs in data/extract.

    python scripts/data_processing/embed.py --mode append     # keeps the collection (default, safe)
    python scripts/data_processing/embed.py --mode fresh      # DELETES the collection first
    python scripts/data_processing/embed.py --mode ocr-only   # only PDFs that had no text before
    python scripts/data_processing/embed.py --tenders 20046891 20046893   # only these tenders (small test corpus)

Point IDs are deterministic, so running append twice does not create duplicates.
"""
from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

import requests

from src.core.config import CFG
from src.core.index import Indexer


def qdrant_is_ready(url: str, timeout_s: float = 3.0) -> bool:
    try:
        return requests.get(url.rstrip("/") + "/readyz", timeout=timeout_s).ok
    except requests.RequestException:
        return False


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build or update the Qdrant index for the tender RAG system.")
    p.add_argument("--mode", choices=["append", "fresh", "ocr-only"], default="append",
                   help="append: keep the collection; fresh: delete and recreate it; ocr-only: only PDFs without text")
    p.add_argument("--collection", default=CFG.qdrant_collection, help="target Qdrant collection")
    p.add_argument("--batch", type=int, default=CFG.embed_batch_size, help="embedding batch size")
    p.add_argument("--flush", type=int, default=CFG.embed_flush_chunks, help="points to buffer before each upsert")
    p.add_argument("--chunk-size", type=int, default=CFG.chunk_size, help="chunk size in characters")
    p.add_argument("--chunk-overlap", type=int, default=CFG.chunk_overlap, help="chunk overlap in characters")
    p.add_argument("--extract-dir", default=str(CFG.extract_dir), help="folder that holds the PDFs")
    p.add_argument("--tenders", nargs="+", metavar="ID", help="only index these tender ids (a small test corpus)")
    p.add_argument("--workers", type=int, default=1,
                   help="processes that read, OCR and chunk the next PDFs while the GPU embeds (1 = one after the other)")
    p.add_argument("--no-health-check", action="store_true", help="skip the Qdrant readiness check")
    p.add_argument("-v", "--verbose", action="store_true")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s | %(levelname)s | %(message)s")

    # Command-line options override the settings for this run only.
    CFG.qdrant_collection = args.collection
    CFG.embed_batch_size = args.batch
    CFG.embed_flush_chunks = args.flush
    CFG.chunk_size = args.chunk_size
    CFG.chunk_overlap = args.chunk_overlap
    extract_dir = Path(args.extract_dir)

    print(f"collection: {CFG.qdrant_collection} | model: {CFG.embed_model} ({CFG.embed_dim}-D) | "
          f"chunks: {CFG.chunk_size}/{CFG.chunk_overlap} | folder: {extract_dir}")

    if not args.no_health_check and not qdrant_is_ready(CFG.qdrant_url):
        sys.exit(f"Qdrant is not ready at {CFG.qdrant_url}/readyz. Start it with: docker compose up -d")

    started = time.time()
    try:
        if args.mode == "ocr-only":
            Indexer(CFG, fresh=False).build_ocr_only(extract_dir=extract_dir, tenders=args.tenders)
        else:
            if args.mode == "fresh":
                print("mode fresh: the existing collection will be deleted and recreated")
            Indexer(CFG, fresh=(args.mode == "fresh")).build(extract_dir=extract_dir, tenders=args.tenders, workers=args.workers)
    except KeyboardInterrupt:
        sys.exit("Interrupted.")
    print(f"Done in {time.time() - started:.1f}s. Next: python scripts/deployment/build_bm25_index.py")


if __name__ == "__main__":
    main()
