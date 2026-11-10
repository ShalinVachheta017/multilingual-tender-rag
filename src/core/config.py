# core/config.py
from __future__ import annotations
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# ROOT should be the project root, not src/
# Path(__file__) = .../src/core/config.py
# parents[2] goes up to project root
ROOT = Path(__file__).resolve().parents[2]


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RAGBOT_", case_sensitive=False)

    # ─── Paths ─────────────────────────────────────────────────────────────
    raw_dir:      Path = ROOT / "data" / "raw"
    extract_dir:  Path = ROOT / "data" / "extract_v1"   # one folder per tender (data/extract is the old flat one)
    metadata_dir: Path = ROOT / "data" / "metadata"
    logs_dir:     Path = ROOT / "data" / "logs"
    state_dir:    Path = ROOT / "data" / "state"

    # If you ever change the filename, the UI/parse step will stay in sync via this:
    metadata_filename: str = "cleaned_metadata.xlsx"

    # ─── Models / Vector DB ────────────────────────────────────────────────
    # Answer model (runs in Ollama). Compare these three later, one at a time:
    #   ollama pull qwen2.5:1.5b   ->  1.0 GB, Apache 2.0  (baseline, the one active now)
    #   ollama pull granite4.1:3b  ->  2.1 GB
    #   ollama pull gemma3:4b      ->  3.4 GB
    # To switch without editing code:  set RAGBOT_LLM_MODEL=gemma3:4b
    llm_model:         str  = "qwen2.5:1.5b"
    # llm_model:       str  = "granite4.1:3b"
    # llm_model:       str  = "gemma3:4b"
    qdrant_url: str = "http://localhost:6333" # health check URL


    # Embedding model. Default: BGE-M3 (1024-D, loads without remote code, no prefixes).
    # Compare other models by setting environment variables, e.g. Jina v3:
    #   RAGBOT_EMBED_MODEL=jinaai/jina-embeddings-v3
    #   RAGBOT_EMBED_REVISION=f1944de8402dcd5f2b03f822a4bc22a7f2de2eb9
    #   RAGBOT_EMBED_TRUST_REMOTE_CODE=true
    #   RAGBOT_EMBED_DOC_PREFIX="search_document: "   RAGBOT_EMBED_QUERY_PREFIX="search_query: "
    # Always use a new RAGBOT_QDRANT_COLLECTION per embedding model: vectors from different models do not mix.
    embed_model:       str  = "BAAI/bge-m3"
    embed_dim:         int  = 1024
    embed_revision:    str | None = None
    embed_trust_remote_code: bool = False
    embed_doc_prefix:  str  = ""
    embed_query_prefix:str  = ""

    qdrant_collection: str  = "tender_bge-m3_v1"

    # ─── Embedding-time knobs ──────────────────────────────────────────────
    embed_batch_size:   int = 32
    embed_flush_chunks: int = 1000

    # ─── Chunking ──────────────────────────────────────────────────────────
    chunk_size:    int = 1000
    chunk_overlap: int = 400

    # ─── Retrieval ────────────────────────────────────────────────────────
    # Keep your existing knobs for compatibility…
    topk_candidate: int   = 100
    final_k:        int   = 16
    min_score:      float = 0.1
    use_hybrid:     bool  = True

    # …and add language routing toggles used by the new retriever
    # Option B: force all retrieval through a German query (EN→DE translation first)
    force_german_retrieval: bool = False
    # Option C: run both (original + German) and fuse with RRF
    dual_query: bool = True

    # ─── Re-ranker (BGE-m3) ───────────────────────────────────────────────
    use_rerank:        bool   = True
    reranker_model:    str    = "BAAI/bge-reranker-v2-m3"
    rerank_keep:       int    = 24
    rerank_weight:     float  = 0.8

    # ─── Convenience properties (don’t override via env) ──────────────────
    @property
    def metadata_path(self) -> Path:
        """Full path to the cleaned metadata Excel used by the UI."""
        return self.metadata_dir / self.metadata_filename

    @property
    def top_k(self) -> int:
        """Unified Top-K accessor (maps to your final_k)."""
        return self.final_k


CFG = AppConfig()
