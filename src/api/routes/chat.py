"""
Chat API routes - RAG-powered question answering
Combines retrieval with LLM generation
"""

from fastapi import APIRouter, HTTPException, status, Depends
from src.api.models.requests import ChatRequest
from src.api.models.responses import ChatResponse, Document, ErrorResponse
from src.api.security import verify_api_key, check_rate_limit
import time
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        200: {"description": "Answer generated successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        401: {"model": ErrorResponse, "description": "Invalid API key"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Ask a question",
    description="Ask a question and get an AI-generated answer based on tender documents",
    dependencies=[Depends(verify_api_key), Depends(check_rate_limit)]
)
async def chat(request: ChatRequest):
    """
    Ask a question and get an AI-generated answer.
    
    - **query**: User question (1-1000 characters)
    - **top_k**: Number of documents to retrieve (1-20, default: 5)
    
    Returns an answer with source documents.
    """
    start_time = time.time()
    
    try:
        from src.core.qa import answer_from_hits, retrieve_candidates

        logger.info(f"Chat request: query='{request.query}', top_k={request.top_k}")

        # Retrieve once, then answer from exactly those sources
        candidates = retrieve_candidates(request.query, limit=request.top_k)
        answer_text = answer_from_hits(request.query, candidates)
        
        # Convert candidates to Document format
        sources = []
        for hit in candidates:
            # Extract ID from payload (proper Hit object structure)
            doc_id = hit.payload.get("id") or hit.payload.get("doc_id") or "unknown"
            
            sources.append(Document(
                id=str(doc_id),
                content=hit.text,
                score=hit.score,
                metadata=hit.payload
            ))
        
        process_time = time.time() - start_time
        
        logger.info(f"Chat completed: {len(sources)} sources used in {process_time:.3f}s")
        
        return ChatResponse(
            query=request.query,
            answer=answer_text,
            sources=sources,
            confidence=None,
            process_time=process_time
        )
        
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}"
        )


@router.get("/chat/health", summary="QA engine health check")
async def chat_health():
    """Check that the QA module imports (models load on the first real request)."""
    try:
        from src.core import qa  # noqa: F401
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"QA engine unhealthy: {e}")
