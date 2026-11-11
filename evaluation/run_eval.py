"""Retrieval check on a question set: does the right tender / file / page show up in the top results?

    $env:RAGBOT_QDRANT_COLLECTION = "tender_bge-m3_v1"
    python evaluation/run_eval.py --dataset evaluation/datasets/g_de_en_48.json --split dev

Deterministic: no LLM involved. Reported separately for German and English, and for all questions together.
Tender-level hit    = a result that comes from a required tender.
Evidence-level hit  = a result from the required file whose page range contains the required page.
The result is written to evaluation/results/<dataset>_<split>_<collection>.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from src.core.config import CFG
from src.core.search import search_hybrid

HERE = Path(__file__).parent
K_LIST = (1, 5, 10)


def evidence_match(hit, files, pages) -> bool:
    payload = hit.payload or {}
    name = Path(payload.get("rel_path", "")).name
    start, end = int(payload.get("page_start") or 0), int(payload.get("page_end") or 0)
    return any(name == f and start <= p <= max(end, start) for f, p in zip(files, pages))


def first_rank(hits, test) -> int | None:
    return next((i for i, h in enumerate(hits, start=1) if test(h)), None)


def summarize(rows: list[dict]) -> dict:
    n_t = len(rows)
    ev = [r for r in rows if r["has_evidence"]]
    out = {"questions": n_t, "with_page_evidence": len(ev)}
    for k in K_LIST:
        out[f"tender_recall@{k}"] = sum(bool(r["tender_rank"]) and r["tender_rank"] <= k for r in rows) / max(n_t, 1)
        out[f"evidence_recall@{k}"] = sum(bool(r["evidence_rank"]) and r["evidence_rank"] <= k for r in ev) / max(len(ev), 1)
    out["tender_mrr@10"] = sum(1 / r["tender_rank"] for r in rows if r["tender_rank"]) / max(n_t, 1)
    out["evidence_mrr@10"] = sum(1 / r["evidence_rank"] for r in ev if r["evidence_rank"]) / max(len(ev), 1)
    return out


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dataset", default=str(HERE / "datasets" / "mini_questions.json"))
    p.add_argument("--split", default="all", choices=["all", "dev", "test"])
    p.add_argument("--verified-only", action="store_true", help="use only questions you confirmed with verify_questions.py (dropped ones are always left out)")
    args = p.parse_args()

    dataset = Path(args.dataset)
    questions = json.loads(dataset.read_text(encoding="utf-8"))["questions"]
    questions = [q for q in questions
                 if q["answerable"] and not q.get("dropped")
                 and (args.split == "all" or q.get("split", "dev") == args.split)
                 and (not args.verified_only or q.get("verified_by_user"))]
    rows = []
    for q in questions:
        hits = search_hybrid(q["question"], limit=max(K_LIST))
        has_ev = bool(q["required_files"])
        rows.append({
            "id": q["id"], "language": q.get("language", "de"), "category": q["category"], "has_evidence": has_ev,
            "tender_rank": first_rank(hits, lambda h: (h.payload or {}).get("dtad_id") in q["required_tender_ids"]),
            "evidence_rank": first_rank(hits, lambda h: evidence_match(h, q["required_files"], q["required_pages"])) if has_ev else None,
        })

    summary = {"all": summarize(rows)}
    for lang in sorted({r["language"] for r in rows}):
        summary[lang] = summarize([r for r in rows if r["language"] == lang])
    print(f"collection: {CFG.qdrant_collection} | dataset {dataset.name} | split {args.split} | {len(rows)} answerable questions")
    for name, s in summary.items():
        print(f"  {name:4} n={s['questions']:3} (pages {s['with_page_evidence']:3}) | tender@5 {s['tender_recall@5']:.3f} | "
              f"page@1 {s['evidence_recall@1']:.3f} @5 {s['evidence_recall@5']:.3f} @10 {s['evidence_recall@10']:.3f} | "
              f"page MRR {s['evidence_mrr@10']:.3f}")

    out = HERE / "results" / f"{dataset.stem}_{args.split}_{CFG.qdrant_collection}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"collection": CFG.qdrant_collection, "dataset": dataset.name, "split": args.split,
                               "summary": summary, "rows": rows}, indent=2), encoding="utf-8")
    print(f"written: {out}")


if __name__ == "__main__":
    sys.exit(main())
