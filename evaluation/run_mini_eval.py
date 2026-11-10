"""Retrieval check on the mini questions: does the right tender / file / page show up in the top results?

    $env:RAGBOT_QDRANT_COLLECTION = "mini_bge-m3"
    python evaluation/run_mini_eval.py            # writes evaluation/results/mini_<collection>.json

Deterministic: no LLM involved.
Tender-level hit    = a result that comes from a required tender.
Evidence-level hit  = a result from the required file whose page range contains the required page.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from src.core.config import CFG
from src.core.search import search_hybrid

DATASET = Path(__file__).parent / "datasets" / "mini_questions.json"
K_LIST = (1, 5, 10)


def evidence_match(hit, files, pages) -> bool:
    payload = hit.payload or {}
    name = Path(payload.get("rel_path", "")).name
    start, end = int(payload.get("page_start") or 0), int(payload.get("page_end") or 0)
    return any(name == f and start <= p <= max(end, start) for f, p in zip(files, pages))


def first_rank(hits, test) -> int | None:
    return next((i for i, h in enumerate(hits, start=1) if test(h)), None)


def main() -> None:
    questions = json.loads(DATASET.read_text(encoding="utf-8"))["questions"]
    rows = []
    for q in (q for q in questions if q["answerable"]):
        hits = search_hybrid(q["question"], limit=max(K_LIST))
        t_rank = first_rank(hits, lambda h: (h.payload or {}).get("dtad_id") in q["required_tender_ids"])
        has_ev = bool(q["required_files"])
        e_rank = first_rank(hits, lambda h: evidence_match(h, q["required_files"], q["required_pages"])) if has_ev else None
        rows.append({"id": q["id"], "category": q["category"], "tender_rank": t_rank,
                     "evidence_rank": e_rank, "has_evidence": has_ev})

    n_t = len(rows)
    n_e = sum(r["has_evidence"] for r in rows)
    print(f"collection: {CFG.qdrant_collection} | {n_t} answerable questions ({n_e} with page-level evidence)")
    print(f"{'id':4} {'category':20} {'tender_rank':12} evidence_rank")
    for r in rows:
        ev = str(r["evidence_rank"]) if r["has_evidence"] else "-"
        print(f"{r['id']:4} {r['category']:20} {str(r['tender_rank']):12} {ev}")

    summary = {}
    for k in K_LIST:
        summary[f"tender_recall@{k}"] = sum(bool(r["tender_rank"]) and r["tender_rank"] <= k for r in rows) / n_t
        summary[f"evidence_recall@{k}"] = (
            sum(bool(r["evidence_rank"]) and r["evidence_rank"] <= k for r in rows if r["has_evidence"]) / max(n_e, 1))
    summary["tender_mrr@10"] = sum(1 / r["tender_rank"] for r in rows if r["tender_rank"]) / n_t
    summary["evidence_mrr@10"] = sum(1 / r["evidence_rank"] for r in rows if r["evidence_rank"]) / max(n_e, 1)
    print({k: round(v, 3) for k, v in summary.items()})

    out = Path(__file__).parent / "results" / f"mini_{CFG.qdrant_collection}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"collection": CFG.qdrant_collection, "summary": summary, "rows": rows}, indent=2),
                   encoding="utf-8")
    print(f"written: {out}")


if __name__ == "__main__":
    sys.exit(main())
