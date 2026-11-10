"""Count PDFs, pages and pages without a text layer (those need OCR) for every tender folder.

    python scripts/data_processing/profile_corpus.py            # prints the table, writes data/logs/corpus_profile.csv
"""
from __future__ import annotations

import csv
import sys

import fitz  # PyMuPDF
from tqdm import tqdm

from src.core.config import CFG

OCR_THRESHOLD = 50  # same rule as PDFLoader: fewer characters than this on a page means "scanned"


def profile_tender(folder) -> dict:
    row = {"tender_id": folder.name, "pdfs": 0, "pages": 0, "scan_pages": 0, "text_chars": 0, "unreadable": 0}
    for pdf in folder.rglob("*.pdf"):
        row["pdfs"] += 1
        try:
            with fitz.open(pdf) as doc:
                for page in doc:
                    n = len((page.get_text() or "").strip())
                    row["pages"] += 1
                    row["text_chars"] += n
                    row["scan_pages"] += n < OCR_THRESHOLD
        except Exception:
            row["unreadable"] += 1
    return row


def main() -> None:
    folders = sorted(p for p in CFG.extract_dir.iterdir() if p.is_dir())
    rows = [profile_tender(f) for f in tqdm(folders, desc="tenders", unit="tender")]
    out = CFG.logs_dir / "corpus_profile.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    total = {k: sum(r[k] for r in rows) for k in ("pdfs", "pages", "scan_pages", "unreadable")}
    print(f"{len(rows)} tenders | {total['pdfs']} PDFs | {total['pages']} pages | "
          f"{total['scan_pages']} pages need OCR ({100 * total['scan_pages'] / max(total['pages'], 1):.1f}%) | "
          f"{total['unreadable']} unreadable PDFs\nwritten: {out}")


if __name__ == "__main__":
    sys.exit(main())
