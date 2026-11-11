"""Check the draft questions one by one. For each question it opens the evidence PDF at the right page in your
browser, shows the expected answer, and asks you to confirm.

    python evaluation/verify_questions.py              # every question that is not verified yet
    python evaluation/verify_questions.py m03 m09      # only these
    python evaluation/verify_questions.py --no-open    # do not open a browser (just print)
    python evaluation/verify_questions.py --dry-run    # ask, but do not save your answers

Answers: y = the expected answer is correct, n = it is wrong (you are asked for a note), s = skip for now, q = quit.
Your answers are saved into evaluation/datasets/mini_questions.json (verified_by_user and, if wrong, a note).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import webbrowser
from pathlib import Path

import pandas as pd

from src.core.config import CFG

DATASET = Path(__file__).parent / "datasets" / "mini_questions.json"
SHOW_COLUMNS = ["titel", "datum", "region", "verfahrensart", "vergabestelle_komplett"]


def find_pdf(tender_id: str, name: str) -> Path | None:
    return next((CFG.extract_dir / tender_id).rglob(name), None)


def open_pdf(path: Path, page: int) -> None:
    webbrowser.open(f"{path.as_uri()}#page={page}")      # Edge and Chrome both honour #page=N


def show_metadata(tender_ids: list[str]) -> None:
    df = pd.read_excel(CFG.metadata_path, dtype=str)
    for tid in tender_ids:
        row = df[df["dtad_id"] == tid]
        print(f"  Excel row for {tid}:")
        if row.empty:
            print("    (not found)")
            continue
        for col in SHOW_COLUMNS:
            print(f"    {col}: {str(row.iloc[0].get(col, ''))[:160]}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("ids", nargs="*", help="question ids, e.g. m01 m05")
    parser.add_argument("--no-open", action="store_true", help="do not open the browser")
    parser.add_argument("--dry-run", action="store_true", help="do not save the answers")
    args = parser.parse_args()

    data = json.loads(DATASET.read_text(encoding="utf-8"))
    todo = [q for q in data["questions"] if (q["id"] in args.ids if args.ids else not q.get("verified_by_user"))]
    print(f"{len(todo)} question(s) to check\n")

    for n, q in enumerate(todo, start=1):
        print("=" * 78)
        print(f"[{n}/{len(todo)}] {q['id']} ({q['category']}, {q['language']})")
        print(f"QUESTION : {q['question']}")
        print(f"EXPECTED : {q['expected_answer']}")
        print(f"EVIDENCE : {q['evidence']}")
        if q["required_files"]:
            for tid, name, page in zip(q["required_tender_ids"], q["required_files"], q["required_pages"]):
                path = find_pdf(tid, name)
                print(f"  PDF page {page}: {path or 'NOT FOUND: ' + name}")
                if path and not args.no_open:
                    open_pdf(path, page)
        elif q["answerable"]:
            show_metadata(q["required_tender_ids"])
        else:
            for tid in q["required_tender_ids"]:
                folder = CFG.extract_dir / tid
                print(f"  Search the PDFs in {folder} for an award decision (Zuschlag erteilt, Auftragnehmer).")
                if not args.no_open and folder.exists():
                    os.startfile(folder)                      # opens the folder in Explorer

        while True:
            answer = input("Is the expected answer correct?  [y] yes  [n] no  [s] skip  [q] quit > ").strip().lower()
            if answer in {"y", "n", "s", "q"}:
                break
        if answer == "q":
            break
        if answer == "y":
            q["verified_by_user"] = True
            q.pop("note", None)
        elif answer == "n":
            q["verified_by_user"] = False
            q["note"] = input("What is wrong or what is the correct answer? > ").strip()

        if not args.dry_run:                                   # save after every question, so quitting loses nothing
            DATASET.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    done = sum(bool(q.get("verified_by_user")) for q in data["questions"])
    print(f"\n{done}/{len(data['questions'])} questions verified.")


if __name__ == "__main__":
    sys.exit(main())
