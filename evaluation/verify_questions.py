"""Check the generated questions. Each question pair (German + English) is checked once: the evidence PDF opens
in your browser at the right page, you see the expected answers, and you confirm, correct or drop it.

    python evaluation/verify_questions.py --dataset evaluation/datasets/g_de_en_48.json --split dev
    python evaluation/verify_questions.py --dataset evaluation/datasets/g_de_en_48.json q11 q12    # only these pairs
    python evaluation/verify_questions.py --no-open        # do not open a browser (just print)
    python evaluation/verify_questions.py --dry-run        # ask, but do not save your answers

Answers:  y  the expected answer is correct
          c  correct it: you type the right answer (German, then English) and it counts as verified
          d  drop this question (bad wording, wrong, or not answerable from the PDF); it is left out of the evaluation
          s  skip for now      q  quit (everything answered so far is saved)
Your answers are saved into the dataset file (verified_by_user, dropped, note).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import webbrowser
from collections import defaultdict
from pathlib import Path

import pandas as pd

from src.core.config import CFG

DEFAULT_DATASET = Path(__file__).parent / "datasets" / "mini_questions.json"
SHOW_COLUMNS = ["titel", "datum", "region", "verfahrensart", "vergabestelle_komplett"]


def find_pdf(tender_id: str, name: str) -> Path | None:
    return next((CFG.extract_dir / tender_id).rglob(name), None)


def open_pdf(path: Path, page: int) -> None:
    webbrowser.open(f"{path.as_uri()}#page={page}")      # Edge and Chrome both honour #page=N


def show_metadata(tender_ids: list[str]) -> None:
    df = pd.read_excel(CFG.metadata_path, dtype=str)
    key = "dtad_id" if "dtad_id" in df.columns else "DTAD-ID"
    for tid in tender_ids:
        row = df[df[key] == tid]
        print(f"  Excel row for {tid}:")
        if row.empty:
            print("    (not found)")
            continue
        for col in SHOW_COLUMNS:
            print(f"    {col}: {str(row.iloc[0].get(col, ''))[:160]}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("ids", nargs="*", help="pair ids (q11) or question ids (m01 or q11_de)")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--split", default="all", choices=["all", "dev", "test"])
    parser.add_argument("--no-open", action="store_true", help="do not open the browser")
    parser.add_argument("--dry-run", action="store_true", help="do not save the answers")
    args = parser.parse_args()

    path = Path(args.dataset)
    data = json.loads(path.read_text(encoding="utf-8"))
    groups: dict[str, list[dict]] = defaultdict(list)
    for q in data["questions"]:
        groups[q.get("pair_id", q["id"])].append(q)

    todo = []
    for gid, qs in groups.items():
        if args.split != "all" and qs[0].get("split", "dev") != args.split:
            continue
        if args.ids:
            if gid in args.ids or any(q["id"] in args.ids for q in qs):
                todo.append(qs)
        elif not all(q.get("verified_by_user") or q.get("dropped") for q in qs):
            todo.append(qs)
    print(f"{len(todo)} question(s) to check in {path.name}\n")

    for n, qs in enumerate(todo, start=1):
        first = qs[0]
        print("=" * 78)
        print(f"[{n}/{len(todo)}] {first.get('pair_id', first['id'])} ({first['category']}, split {first.get('split', '-')})")
        for q in qs:
            print(f"  {q['language'].upper()} QUESTION: {q['question']}")
            print(f"  {q['language'].upper()} EXPECTED: {q['expected_answer']}")
        print(f"EVIDENCE : {first['evidence']}")
        if first.get("review_hint"):
            print(f"HINT     : {first['review_hint']}")
        if first["required_files"]:
            for tid, name, page in zip(first["required_tender_ids"], first["required_files"], first["required_pages"]):
                pdf = find_pdf(tid, name)
                print(f"  PDF page {page}: {pdf or 'NOT FOUND: ' + name}")
                if pdf and not args.no_open:
                    open_pdf(pdf, page)
        elif first["answerable"]:
            show_metadata(first["required_tender_ids"])
        else:
            for tid in first["required_tender_ids"]:
                folder = CFG.extract_dir / tid
                print(f"  Search the PDFs in {folder} for the answer (award decision, number of bids). If it is not there, the expected answer is right.")
                if not args.no_open and folder.exists():
                    os.startfile(folder)                      # opens the folder in Explorer

        while True:
            answer = input("[y] correct  [c] correct it  [d] drop  [s] skip  [q] quit > ").strip().lower()
            if answer in {"y", "c", "d", "s", "q"}:
                break
        if answer == "q":
            break
        if answer == "y":
            for q in qs:
                q.update(verified_by_user=True, dropped=False)
        elif answer == "c":
            for q in qs:
                new = input(f"  Correct {q['language'].upper()} answer > ").strip()
                if new:
                    q["expected_answer"] = new
                q.update(verified_by_user=True, dropped=False)
        elif answer == "d":
            note = input("  Why (optional) > ").strip()
            for q in qs:
                q.update(verified_by_user=False, dropped=True, note=note)

        if not args.dry_run:                                   # save after every question, so quitting loses nothing
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    questions = data["questions"]
    print(f"\n{sum(bool(q.get('verified_by_user')) for q in questions)} verified, "
          f"{sum(bool(q.get('dropped')) for q in questions)} dropped, of {len(questions)} questions.")


if __name__ == "__main__":
    sys.exit(main())
