"""Step 1 of 3: prepare the files.

Unzips every tender in data/raw into data/extract_v1/<tender_id>/ (one folder per tender), copies loose files, and cleans the
metadata Excel. It does NOT build the index; the next steps are:

    python scripts/data_processing/embed.py --mode append
    python scripts/deployment/build_bm25_index.py
"""
from __future__ import annotations

import argparse
import logging
import shutil
import sys
from datetime import datetime

from src.core.config import CFG
from src.core.io import ExcelCleaner, ZipIngestor

LOOSE_EXTENSIONS = {".pdf", ".docx", ".d83", ".dwg", ".jpg", ".png", ".tiff"}


def copy_loose_files(only: list[str] | None = None) -> int:
    """Copy non-zip files from data/raw/<tender_id>/ to the same tender folder in the extract dir."""
    copied = 0
    for src in CFG.raw_dir.rglob("*"):
        if not src.is_file() or src.suffix.lower() not in LOOSE_EXTENSIONS:
            continue
        rel = src.relative_to(CFG.raw_dir)
        if len(rel.parts) < 2 or (only and rel.parts[0] not in only):   # files must sit inside a tender folder
            continue
        dst = CFG.extract_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
                shutil.copy2(src, dst)
                copied += 1
        except Exception:
            logging.exception("Copy failed for %s", src)
    return copied


def main() -> None:
    parser = argparse.ArgumentParser(description="Unzip tenders, copy loose files, clean the metadata Excel.")
    parser.add_argument("--only", nargs="+", metavar="ID", help="only these tender ids")
    parser.add_argument("--force", action="store_true", help="unpack tenders again even if their folder exists")
    parser.add_argument("--skip-clean", action="store_true", help="do not clean the metadata Excel")
    parser.add_argument("-v", "--verbose", action="store_true", help="also log to the console")
    args = parser.parse_args()

    CFG.logs_dir.mkdir(parents=True, exist_ok=True)
    handlers = [logging.FileHandler(CFG.logs_dir / f"ingest_run_{datetime.now():%Y%m%d_%H%M%S}.log")]
    if args.verbose:
        handlers.append(logging.StreamHandler(sys.stdout))
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s", handlers=handlers)

    print("1/3 Unzipping tender archives (nested zips included) ...")
    extracted = ZipIngestor().run(only=args.only, force=args.force)
    print(f"    {extracted} files extracted")

    print("2/3 Copying loose files from data/raw to the extract folder ...")
    print(f"    {copy_loose_files(args.only)} files copied")

    if not args.skip_clean:
        print("3/3 Cleaning the metadata Excel ...")
        try:
            print(f"    written: {ExcelCleaner().run()}")
        except FileNotFoundError:
            print("    no Excel file found in data/raw, skipped")

    pdf_count = sum(1 for _ in CFG.extract_dir.rglob("*.pdf"))
    print(f"\nDone: {pdf_count} PDFs ready in {CFG.extract_dir}")
    print("Next: python scripts/data_processing/embed.py --mode append")


if __name__ == "__main__":
    main()
