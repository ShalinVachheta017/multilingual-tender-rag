"""Step 2b of 3: build one Qdrant collection (and its keyword file) per embedding model from the saved chunks.

    python scripts/data_processing/build_collections.py                    # all models
    python scripts/data_processing/build_collections.py bge-m3 jina-v3     # only some
    python scripts/data_processing/build_collections.py --prefix mini --version "" --tenders 20046891 20046904

Needs the chunk file from prepare_chunks.py. Everything here runs on the GPU: no PDF is read and no OCR runs.
Each model runs in its own process, so its settings never leak into the next one. Safe to run again:
point ids are stable, so nothing is duplicated.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

from src.core.awake import keep_awake
from src.core.config import CFG
from src.core.embedder_presets import PRESETS, env_for

ROOT = Path(__file__).resolve().parents[2]


def run(script: str, args: list[str], env_extra: dict[str, str]) -> None:
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", **env_extra}
    subprocess.run([sys.executable, str(ROOT / script), *args], cwd=ROOT, env=env, check=True)


def main() -> None:
    p = argparse.ArgumentParser(description="Embed the saved chunks with each model into its own collection.")
    p.add_argument("models", nargs="*", help=f"any of: {', '.join(PRESETS)} (default: all)")
    p.add_argument("--prefix", default="tender", help="collection name prefix (tender -> tender_bge-m3_v1)")
    p.add_argument("--version", default="_v1", help="collection name suffix")
    p.add_argument("--tenders", nargs="+", metavar="ID", help="only these tenders (for a small test corpus)")
    p.add_argument("--chunks-file", default=str(CFG.chunks_path))
    args = p.parse_args()

    if not Path(args.chunks_file).exists():
        sys.exit(f"{args.chunks_file} not found. Run scripts/data_processing/prepare_chunks.py first.")
    keep_awake()
    for name in args.models or list(PRESETS):
        env = env_for(name, args.prefix, args.version)
        print(f"\n===== {name} -> {env['RAGBOT_QDRANT_COLLECTION']} =====", flush=True)
        started = time.time()
        embed_args = ["--mode", "append", "--from-chunks", "--chunks-file", args.chunks_file]
        if args.tenders:
            embed_args += ["--tenders", *args.tenders]
        run("scripts/data_processing/embed.py", embed_args, env)
        run("scripts/deployment/build_bm25_index.py", [], env)
        print(f"{name} finished in {time.time() - started:.0f}s", flush=True)


if __name__ == "__main__":
    main()
