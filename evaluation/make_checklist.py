"""Write evaluation/verify_mini.md: a checklist to confirm every draft answer in the source PDF.

    python evaluation/make_checklist.py

For each question it shows the expected answer, the PDF to open (full path), the page, and the text the
index holds around the quoted evidence. Open the PDF at that page, confirm the answer, then set
"verified_by_user": true for that question in evaluation/datasets/mini_questions.json.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from qdrant_client import QdrantClient

from src.core.config import CFG

DATASET = Path(__file__).parent / "datasets" / "mini_questions.json"
OUT = Path(__file__).parent / "verify_mini.md"
COLLECTION = "mini_bge-m3"   # any mini collection works: the text and the paths are identical


def main() -> None:
    questions = json.loads(DATASET.read_text(encoding="utf-8"))["questions"]
    client = QdrantClient(url=CFG.qdrant_url, prefer_grpc=False)
    points, _ = client.scroll(COLLECTION, limit=5000, with_payload=True)
    lines = ["# Verify the mini questions", "",
             "Open each PDF at the page, confirm the expected answer, then set `verified_by_user` to `true` "
             "in `evaluation/datasets/mini_questions.json`.", ""]
    for q in questions:
        lines += [f"## {q['id']} ({q['category']}, {q['language']})", "", f"**Question:** {q['question']}", "",
                  f"**Expected answer:** {q['expected_answer']}", ""]
        if not q["required_files"]:
            lines += [f"**Source:** {q['evidence']}", ""]
            if q["answerable"] is False:
                lines += ["**Check:** search the tender's PDFs for an award decision (Zuschlag erteilt, Auftragnehmer). "
                          "If none is stated, the expected answer is right.", ""]
            continue
        quote = re.search(r"'([^']+)'", q["evidence"])
        quote = quote.group(1) if quote else ""
        for tender, name, page in zip(q["required_tender_ids"], q["required_files"], q["required_pages"]):
            hit = next((p for p in points if p.payload["dtad_id"] == tender
                        and Path(p.payload["rel_path"]).name == name
                        and int(p.payload["page_start"]) <= page <= int(p.payload["page_end"])
                        and (not quote or quote in re.sub(r"\s+", " ", p.payload["text"]))), None)
            path = (CFG.extract_dir / hit.payload["rel_path"]) if hit else None
            lines += [f"- **PDF:** `{path or name}`", f"- **Page:** {page}"]
            if hit:
                text = re.sub(r"\s+", " ", hit.payload["text"])
                i = max(text.find(quote), 0)
                lines += [f"- **Text in the index:** ...{text[max(0, i - 150): i + 250]}..."]
            else:
                lines += ["- **Text in the index:** not found, check this one by hand"]
            lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"written: {OUT}")


if __name__ == "__main__":
    sys.exit(main())
