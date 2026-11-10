"""Retrieval: dense (Qdrant) + BM25, fused with Reciprocal Rank Fusion (RRF).

Every search function returns objects with `.id`, `.score` and `.payload`.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, Dict, List, Optional, Sequence

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from sentence_transformers import SentenceTransformer

from .config import CFG

logger = logging.getLogger(__name__)

@dataclass
class ScoredHit:
    """A search result that did not come straight from a Qdrant vector search (e.g. a BM25 hit)."""
    id: Any
    score: float
    payload: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Shared resources (created once)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _client() -> QdrantClient:
    return QdrantClient(url=CFG.qdrant_url, prefer_grpc=False, timeout=60.0)


@lru_cache(maxsize=1)
def _embedder() -> SentenceTransformer:
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return SentenceTransformer(CFG.embed_model, revision=CFG.embed_revision,
                               trust_remote_code=CFG.embed_trust_remote_code, device=device)


@lru_cache(maxsize=1)
def _check_collection() -> None:
    """Fail early if the collection is missing or built with a different vector size.

    An exception is not cached, so this retries until Qdrant and the collection exist.
    """
    info = _client().get_collection(CFG.qdrant_collection)  # raises if missing
    size = info.config.params.vectors.size
    if size != CFG.embed_dim:
        raise RuntimeError(
            f"Collection '{CFG.qdrant_collection}' has vector size {size}, "
            f"but the embedding model gives {CFG.embed_dim}. Rebuild the index."
        )


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

def detect_tender_id(query: str) -> Optional[str]:
    """Return the 8-digit tender id in the query ("DTAD-ID 20046891", "Tender ...", "Vergabe ...", or just the number)."""
    match = re.search(r"(?:DTAD-ID|Tender|Vergabe)\s*(\d{8})", query, re.IGNORECASE)
    if match:
        return match.group(1)
    if re.fullmatch(r"\d{8}", query.strip()):
        return query.strip()
    return None


@lru_cache(maxsize=1000)
def _embed_cached(text: str) -> tuple:
    vec = _embedder().encode([CFG.embed_query_prefix + text], normalize_embeddings=True, convert_to_numpy=True)[0]
    return tuple(float(x) for x in vec)


def embed_query(text: str) -> List[float]:
    """Embed a user query (cached, so repeated questions are instant)."""
    return list(_embed_cached(text))


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

def search_dense(query_text: str, limit: Optional[int] = None, min_score: Optional[float] = None):
    """Vector search in Qdrant. A tender id in the query first tries a filter on that tender."""
    _check_collection()
    limit = int(limit or CFG.topk_candidate)
    qv = embed_query(query_text)

    tender_id = detect_tender_id(query_text)
    if tender_id:
        try:
            res = _client().query_points(
                collection_name=CFG.qdrant_collection,
                query=qv,
                query_filter=qmodels.Filter(
                    must=[qmodels.FieldCondition(key="dtad_id", match=qmodels.MatchValue(value=tender_id))]
                ),
                limit=limit,
                with_payload=True,
            ).points
            if res:
                return res
        except Exception as e:
            logger.warning("Tender-id filter failed, using normal search: %s", e)

    res = _client().query_points(
        collection_name=CFG.qdrant_collection, query=qv, limit=limit, with_payload=True
    ).points
    threshold = CFG.min_score if min_score is None else float(min_score)
    if threshold > 0:
        res = [r for r in res if r.score is not None and r.score >= threshold]
    return res


def rrf(result_sets: List[Sequence], k: int = 60) -> list:
    """Reciprocal Rank Fusion: merge ranked lists (items need `.id`) into one ranked list."""
    scores: Dict[str, float] = {}
    items: Dict[str, Any] = {}
    for results in result_sets:
        for rank, item in enumerate(results, start=1):
            pid = str(item.id)
            scores[pid] = scores.get(pid, 0.0) + 1.0 / (k + rank)
            items.setdefault(pid, item)
    return sorted(items.values(), key=lambda item: scores[str(item.id)], reverse=True)


def _search_bm25_hits(query_text: str, limit: int) -> List[ScoredHit]:
    """BM25 search, then fetch the matching points (text + payload) from Qdrant."""
    from .hybrid_search import search_bm25

    bm25 = search_bm25(query_text, top_k=limit)  # [(point_id, bm25_score), ...] best first
    if not bm25:
        return []
    points = {str(p.id): p for p in _client().retrieve(
        collection_name=CFG.qdrant_collection, ids=[pid for pid, _ in bm25], with_payload=True)}
    # Keep BM25's order (Qdrant's retrieve() does not).
    return [ScoredHit(id=pid, score=score, payload=points[str(pid)].payload or {})
            for pid, score in bm25 if str(pid) in points]


def search_hybrid(query_text: str, limit: Optional[int] = None):
    """Dense + BM25, fused with RRF. If BM25 is unavailable, returns dense results only."""
    limit = int(limit or CFG.topk_candidate)
    dense = search_dense(query_text, limit=limit)
    try:
        bm25 = _search_bm25_hits(query_text, limit)
    except Exception as e:
        logger.warning("BM25 failed, using dense only: %s", e)
        return dense[:limit]
    tender_id = detect_tender_id(query_text)
    if tender_id:  # a question about one tender must not be answered from another one
        bm25 = [h for h in bm25 if h.payload.get("dtad_id") == tender_id]
    if not bm25:
        return dense[:limit]
    return rrf([dense, bm25])[:limit]
