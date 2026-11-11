"""Compare the embedding models on the mini questions, one after the other.

    python evaluation/compare_embedders.py                 # all models below
    python evaluation/compare_embedders.py bge-m3 jina-v3  # only some

For each model it builds that collection's keyword file, runs evaluation/run_mini_eval.py with the model's own
settings, and prints one table. The collections must already exist (built with embed.py and the same settings).
Each model runs in its own process, so settings never leak from one to the next.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QWEN_QUERY = "Instruct: Given a question about a German public tender, retrieve the passages that answer it\nQuery: "

MODELS = {
    "bge-m3": {"RAGBOT_QDRANT_COLLECTION": "mini_bge-m3"},
    "qwen3-0.6b": {
        "RAGBOT_QDRANT_COLLECTION": "mini_qwen3-0.6b",
        "RAGBOT_EMBED_MODEL": "Qwen/Qwen3-Embedding-0.6B",
        "RAGBOT_EMBED_QUERY_PREFIX": QWEN_QUERY,
    },
    "jina-v3": {
        "RAGBOT_QDRANT_COLLECTION": "mini_jina-v3",
        "RAGBOT_EMBED_MODEL": "jinaai/jina-embeddings-v3",
        "RAGBOT_EMBED_REVISION": "f1944de8402dcd5f2b03f822a4bc22a7f2de2eb9",
        "RAGBOT_EMBED_TRUST_REMOTE_CODE": "true",
        "RAGBOT_EMBED_DOC_PREFIX": "search_document: ",
        "RAGBOT_EMBED_QUERY_PREFIX": "search_query: ",
    },
}
COLUMNS = ["tender_recall@5", "evidence_recall@1", "evidence_recall@5", "evidence_recall@10", "evidence_mrr@10"]


def run(script: str, env_extra: dict) -> None:
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", **env_extra}
    subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, env=env, check=True)


def main() -> None:
    wanted = sys.argv[1:] or list(MODELS)
    for name in wanted:
        print(f"\n===== {name} =====", flush=True)
        run("scripts/deployment/build_bm25_index.py", MODELS[name])
        run("evaluation/run_mini_eval.py", MODELS[name])

    print("\n" + "model".ljust(14) + "".join(c.rjust(20) for c in COLUMNS))
    for name in wanted:
        path = ROOT / "evaluation" / "results" / f"mini_{MODELS[name]['RAGBOT_QDRANT_COLLECTION']}.json"
        summary = json.loads(path.read_text(encoding="utf-8"))["summary"]
        print(name.ljust(14) + "".join(f"{summary[c]:20.3f}" for c in COLUMNS))


if __name__ == "__main__":
    main()
