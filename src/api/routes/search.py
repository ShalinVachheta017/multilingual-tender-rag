"""
Search API routes - Hybrid search endpoint
Integrates BM25 + Dense vector search with RRF fusion
"""

from fastapi import APIRouter, HTTPException, status, Depends
from src.api.models.requests import SearchRequest
from src.api.models.responses import SearchResponse, Document, ErrorResponse
from src.api.security import verify_api_key, check_rate_limit
import time
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/search",
    response_model=SearchResponse,
    responses={
        200: {"description": "Search results returned successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        401: {"model": ErrorResponse, "description": "Invalid API key"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Search documents",
    description="Search tender documents using hybrid search (BM25 + Dense vectors)",
    dependencies=[Depends(verify_api_key), Depends(check_rate_limit)]
)
async def search_documents(request: SearchRequest):
    """
    Search documents using hybrid search.
    
    - **query**: Search query text (1-500 characters)
    - **top_k**: Number of results to return (1-20, default: 5)
    - **search_mode**: hybrid (recommended), dense, or bm25
    - **score_threshold**: Minimum score threshold (optional, dynamic by default)
    
    Returns ranked documents with relevance scores.
    """
    start_time = time.time()
    
    try:
        from src.core import hybrid_search, search

        logger.info(f"Search request: query='{request.query}', mode={request.search_mode}, top_k={request.top_k}")

        if request.search_mode == "hybrid":
            points = search.search_hybrid(request.query, limit=request.top_k)
        elif request.search_mode == "dense":
            points = search.search_dense(request.query, limit=request.top_k)
        elif request.search_mode == "bm25":
            points = []  # BM25 only returns (id, score); the content is not fetched in this mode
            bm25_ids = hybrid_search.search_bm25(request.query, top_k=request.top_k)
        else:
            raise ValueError(f"Invalid search mode: {request.search_mode}")

        if request.search_mode == "bm25":
            documents = [Document(id=str(i), content="", score=score, metadata={}) for i, score in bm25_ids]
        else:
            documents = [
                Document(
                    id=str(p.id),
                    content=(p.payload or {}).get("text", ""),
                    score=float(p.score or 0.0),
                    metadata={k: v for k, v in (p.payload or {}).items() if k not in ("text", "doc_id")},
                )
                for p in points
            ]

        process_time = time.time() - start_time
        
        logger.info(f"Search completed: {len(documents)} results in {process_time:.3f}s")
        
        return SearchResponse(
            query=request.query,
            results=documents,
            total_results=len(documents),
            search_mode=request.search_mode,
            process_time=process_time
        )
        
    except Exception as e:
        logger.error(f"Search error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.get("/search/health", summary="Search engine health check")
async def search_health():
    """Check that the search modules import (models load on the first real request)."""
    try:
        from src.core import hybrid_search, search  # noqa: F401
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Search engine unhealthy: {e}")
