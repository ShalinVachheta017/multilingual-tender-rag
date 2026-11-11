"""The embedding models we compare, as environment settings (they are read by src.core.config).

A "preset" is everything that differs between models: the model name, its revision, whether it needs
remote code, and the text put in front of documents and questions. The collection name is not part of
the preset: vectors from different models never share a collection.
"""
from __future__ import annotations

QWEN_QUERY = "Instruct: Given a question about a German public tender, retrieve the passages that answer it\nQuery: "

PRESETS: dict[str, dict[str, str]] = {
    "bge-m3": {},   # the defaults in config.py: BAAI/bge-m3, no prefixes, no remote code
    "qwen3-0.6b": {
        "RAGBOT_EMBED_MODEL": "Qwen/Qwen3-Embedding-0.6B",
        "RAGBOT_EMBED_BATCH_SIZE": "8",
        "RAGBOT_EMBED_QUERY_PREFIX": QWEN_QUERY,
    },
    "jina-v3": {
        "RAGBOT_EMBED_MODEL": "jinaai/jina-embeddings-v3",
        "RAGBOT_EMBED_BATCH_SIZE": "8",
        "RAGBOT_EMBED_REVISION": "f1944de8402dcd5f2b03f822a4bc22a7f2de2eb9",
        "RAGBOT_EMBED_TRUST_REMOTE_CODE": "true",
        "RAGBOT_EMBED_DOC_PREFIX": "search_document: ",
        "RAGBOT_EMBED_QUERY_PREFIX": "search_query: ",
    },
}


def env_for(name: str, prefix: str = "tender", version: str = "_v1") -> dict[str, str]:
    """Environment settings for one model, including its own collection name, e.g. tender_bge-m3_v1."""
    return {**PRESETS[name], "RAGBOT_QDRANT_COLLECTION": f"{prefix}_{name}{version}"}
