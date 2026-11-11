"""Step 2a of 3: read, OCR and chunk every PDF once, and save the chunks to one file.

    python scripts/data_processing/prepare_chunks.py --workers 12
    python scripts/data_processing/prepare_chunks.py --tenders 20046891 20046904   # a few tenders only

The result (data/chunks/chunks_s<size>_o<overlap>.jsonl) is then embedded by as many models as you like with
    python scripts/data_processing/embed.py --from-chunks
without reading or OCR-ing a single PDF again. That is the slow, CPU-bound half of indexing, done once.
The file is written to a temporary name first and renamed at the end, so an interrupted run leaves no half file.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
from pathlib import Path

from tqdm import tqdm

from src.core.awake import keep_awake
from src.core.config import CFG
from src.core.prepare import init_worker, prepare_record


def main() -> None:
    p = argparse.ArgumentParser(description="Read, OCR and chunk all PDFs once and save the chunks.")
    p.add_argument("--extract-dir", default=str(CFG.extract_dir), help="folder with one sub-folder per tender")
    p.add_argument("--out", default=None, help="output file (default: data/chunks/chunks_s<size>_o<overlap>.jsonl)")
    p.add_argument("--workers", type=int, default=8, help="processes that read and OCR in parallel")
    p.add_argument("--chunk-size", type=int, default=CFG.chunk_size)
    p.add_argument("--chunk-overlap", type=int, default=CFG.chunk_overlap)
    p.add_argument("--tenders", nargs="+", metavar="ID", help="only these tender ids")
    args = p.parse_args()

    CFG.chunk_size, CFG.chunk_overlap = args.chunk_size, args.chunk_overlap
    base = Path(args.extract_dir)
    out = Path(args.out or CFG.chunks_path)
    roots = [base / t for t in args.tenders] if args.tenders else [base]
    pdfs = sorted(p for r in roots for p in r.rglob("*.pdf") if p.is_file())   # a folder can be named "x.pdf"
    if not pdfs:
        sys.exit(f"No PDFs found in {base}")
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".jsonl.tmp")
    print(f"{len(pdfs)} PDFs | chunks {args.chunk_size}/{args.chunk_overlap} | {args.workers} workers -> {out}")

    keep_awake()
    started = time.time()
    n_chunks = n_ocr = 0
    problems: list[str] = []
    empty = 0
    with ProcessPoolExecutor(max_workers=args.workers, initializer=init_worker) as pool, \
            tmp.open("w", encoding="utf-8") as f:
        results = pool.map(prepare_record, pdfs, repeat(base), repeat(args.chunk_size), repeat(args.chunk_overlap))
        for rec in tqdm(results, total=len(pdfs), desc="PDFs", unit="file"):
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n_chunks += len(rec["chunks"])
            n_ocr += rec["ocr_pages"]
            empty += not rec["chunks"] and not rec["error"]
            if rec["error"]:
                problems.append(f"{rec['rel_path']}: {rec['error']}")
    tmp.replace(out)

    print(f"\nDone in {time.time() - started:.0f}s: {len(pdfs)} PDFs, {n_chunks} chunks, {n_ocr} pages OCR'd, "
          f"{empty} PDFs without any text, {len(problems)} with errors")
    for line in problems[:10]:
        print("  error:", line)
    print(f"written: {out}\nNext: python scripts/data_processing/build_collections.py")


if __name__ == "__main__":
    sys.exit(main())
