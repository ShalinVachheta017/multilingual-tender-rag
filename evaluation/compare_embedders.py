"""Compare the embedding models on a question set, one after the other.

    python evaluation/compare_embedders.py                                   # mini collections, mini questions
    python evaluation/compare_embedders.py --prefix tender --version _v1 \
        --dataset evaluation/datasets/g_de_en_48.json --split dev            # full corpus, 48 questions
    python evaluation/compare_embedders.py bge-m3 jina-v3                    # only some models

For each model it builds that collection's keyword file, runs evaluation/run_eval.py with the model's own
settings (src/core/embedder_presets.py), and prints one table per language. The collections must already exist.
Each model runs in its own process, so settings never leak from one to the next.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from src.core.embedder_presets import PRESETS, env_for

ROOT = Path(__file__).resolve().parents[1]
COLUMNS = ["tender_recall@5", "evidence_recall@1", "evidence_recall@5", "evidence_recall@10", "evidence_mrr@10"]


def run(script: str, args: list[str], env_extra: dict) -> None:
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", **env_extra}
    subprocess.run([sys.executable, str(ROOT / script), *args], cwd=ROOT, env=env, check=True)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("models", nargs="*", help=f"any of: {', '.join(PRESETS)} (default: all)")
    p.add_argument("--prefix", default="mini")
    p.add_argument("--version", default="")
    p.add_argument("--dataset", default="evaluation/datasets/mini_questions.json")
    p.add_argument("--split", default="all", choices=["all", "dev", "test"])
    args = p.parse_args()

    names = args.models or list(PRESETS)
    for name in names:
        env = env_for(name, args.prefix, args.version)
        print(f"\n===== {name} ({env['RAGBOT_QDRANT_COLLECTION']}) =====", flush=True)
        run("scripts/deployment/build_bm25_index.py", [], env)
        run("evaluation/run_eval.py", ["--dataset", args.dataset, "--split", args.split], env)

    results = {}
    for name in names:
        collection = env_for(name, args.prefix, args.version)["RAGBOT_QDRANT_COLLECTION"]
        path = ROOT / "evaluation" / "results" / f"{Path(args.dataset).stem}_{args.split}_{collection}.json"
        results[name] = json.loads(path.read_text(encoding="utf-8"))["summary"]
    for group in results[names[0]]:
        print(f"\n[{group}]  n={results[names[0]][group]['questions']}")
        print("model".ljust(14) + "".join(c.rjust(20) for c in COLUMNS))
        for name in names:
            print(name.ljust(14) + "".join(f"{results[name][group][c]:20.3f}" for c in COLUMNS))


if __name__ == "__main__":
    main()
