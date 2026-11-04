"""Question answering: retrieve chunks, optionally rerank them, then ask the local LLM.

    hits = retrieve_candidates(question)          # search (+ translate, + rerank)
    answer = answer_from_hits(question, hits)     # build the prompt and call Ollama
    answer = answer_query(question)               # both steps in one call
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from langdetect import detect

from .config import CFG
from .search import rrf, search_dense, search_hybrid

logger = logging.getLogger(__name__)

MAX_CONTEXT_CHARS = 3000  # keeps the prompt small enough that Ollama does not time out


@dataclass
class Hit:
    text: str
    score: float
    payload: Dict[str, Any]
    page: Optional[int] = None
    source: str = ""


def _to_hit(point) -> Hit:
    payload = point.payload or {}
    return Hit(
        text=(payload.get("text") or payload.get("chunk_text") or "")[:2000],
        score=float(point.score or 0.0),
        payload=payload,
        page=payload.get("page_start") or payload.get("page"),
        source=payload.get("source_path") or payload.get("source") or "",
    )


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------

def _translate_to_de(text: str) -> str:
    """Translate to German with the local LLM; return the input unchanged if that fails."""
    try:
        import ollama
        prompt = ("Übersetze exakt ins Deutsche. Erhalte Namen, Zahlen, Fachbegriffe. "
                  "Nicht zusammenfassen oder umformulieren.\n\nTEXT:\n" + text + "\n\nDEUTSCH:")
        out = ollama.chat(model=CFG.llm_model, messages=[{"role": "user", "content": prompt}])
        return out["message"]["content"].strip()
    except Exception as e:
        logger.warning("Translation to German failed, using the original question: %s", e)
        return text


@lru_cache(maxsize=1)
def _reranker():
    from FlagEmbedding import FlagReranker
    return FlagReranker(CFG.reranker_model, use_fp16=True)


def _rerank(question: str, hits: List[Hit], cfg) -> List[Hit]:
    """Blend reranker score and search score, keep the best `rerank_keep`. On failure keep the search order."""
    try:
        pairs = [(question, h.text[:1800]) for h in hits]
        scores = _reranker().compute_score(pairs, normalize=True)
    except Exception as e:
        logger.warning("Reranker unavailable, keeping search order: %s", e)
        return hits
    w = float(cfg.rerank_weight)
    blended = sorted(zip(hits, scores), key=lambda t: w * float(t[1]) + (1.0 - w) * t[0].score, reverse=True)
    return [h for h, _ in blended[: int(cfg.rerank_keep)]]


def retrieve_candidates(user_text: str, cfg=CFG, limit: Optional[int] = None) -> List[Hit]:
    """Search (hybrid or dense), optionally also with a German translation, then rerank and cut to `final_k`."""
    limit = int(limit or cfg.top_k)
    search = search_hybrid if cfg.use_hybrid else search_dense

    queries = [user_text]
    if cfg.force_german_retrieval or cfg.dual_query:
        try:
            is_german = detect(user_text) == "de"
        except Exception:
            is_german = True
        german = user_text if is_german else _translate_to_de(user_text)
        queries = [user_text, german] if cfg.dual_query else [german]

    result_sets = [search(q, limit) for q in dict.fromkeys(queries)]  # drops a duplicate query
    points = result_sets[0] if len(result_sets) == 1 else rrf(result_sets)[:limit]
    hits = [_to_hit(p) for p in points]

    is_id_lookup = bool(re.fullmatch(r"\d{8}", user_text.strip()))  # an exact id needs no reranking
    if cfg.use_rerank and hits and not is_id_lookup:
        hits = _rerank(user_text, hits, cfg)
    return hits[: int(cfg.final_k)]


# ---------------------------------------------------------------------------
# Answering
# ---------------------------------------------------------------------------

def _build_context(hits: List[Hit]) -> str:
    blocks = []
    for h in hits:
        snippet = h.text.strip()
        if not snippet:
            continue
        name = Path(h.source).name or "source"
        start, end = h.payload.get("page_start"), h.payload.get("page_end")
        cite = f"[{name}:p{start}-{end}]" if start is not None and end is not None else f"[{name}]"
        blocks.append(f"{cite}\n{snippet}")
    context = "\n\n---\n\n".join(blocks) or "(no context)"
    if len(context) > MAX_CONTEXT_CHARS:
        context = context[:MAX_CONTEXT_CHARS] + "\n...[context truncated]"
    return context


def answer_from_hits(question: str, hits: List[Hit]) -> str:
    """Ask the LLM to answer from the given hits only."""
    prompt = (
        "Beantworte die Frage NUR mit dem bereitgestellten Kontext. "
        "Wenn es nicht im Kontext steht, sage ehrlich, dass du es nicht weißt. "
        "Antworte auf Deutsch, wenn die Frage Deutsch ist; sonst antworte in der Sprache der Frage. "
        "Sei präzise und nenne die Quelle in eckigen Klammern.\n\n"
        f"Kontext:\n{_build_context(hits)}\n\nFrage: {question}\nAntwort:"
    )
    return _ask_llm(prompt)


def answer_query(user_text: str, cfg=CFG) -> str:
    """Retrieve and answer in one call."""
    return answer_from_hits(user_text, retrieve_candidates(user_text, cfg))


def _ask_llm(prompt: str) -> str:
    """Call Ollama with the Python client; if that fails, try its HTTP API."""
    options = {"num_predict": 256, "temperature": 0.2, "top_p": 0.9}
    try:
        import ollama
        reply = ollama.chat(model=CFG.llm_model, messages=[{"role": "user", "content": prompt}], options=options)
        return reply["message"]["content"].strip()
    except Exception as client_error:
        try:
            r = requests.post("http://localhost:11434/api/generate", timeout=60,
                              json={"model": CFG.llm_model, "prompt": prompt, "options": options, "stream": False})
            r.raise_for_status()
            return (r.json().get("response") or "").strip() or "[LLM returned empty response]"
        except Exception as http_error:
            return (f"[LLM unavailable - Ollama: {client_error}, API: {http_error}] "
                    "Based on the context, I found relevant documents but cannot generate an answer.")
