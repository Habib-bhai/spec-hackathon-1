"""
Chat router for RAG chatbot API.

Handles chat requests with context-aware responses using
retrieval-augmented generation.
"""

import json
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from api.models.chat import ChatRequest, ChatResponse
from api.services import RAGService, VectorService
from api.dependencies import get_rag_service
from api.db import get_connection
import asyncpg

logger = logging.getLogger(__name__)

router = APIRouter()


@router.options("/")
async def chat_options():
    """Handle CORS preflight requests for chat endpoint."""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        }
    )


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service),
) -> ChatResponse:
    """
    Process a chat message and return AI response.
    
    This endpoint:
    1. Searches for relevant textbook content
    2. Generates a contextual response using Gemini
    3. Saves the conversation to the database
    4. Returns the response with source citations
    
    Args:
        request: Chat request with message and context
        rag_service: RAG service dependency
        
    Returns:
        ChatResponse with answer and sources
    """
    try:
        logger.info(f"Chat request: session_id={request.session_id}, user_id={request.user_id}")
        
        # Get or create session
        session_id = request.session_id
        if session_id is None:
            # Create new session
            async with get_connection() as conn:
                session_id = await conn.fetchval(
                    "INSERT INTO chat_sessions (user_id) VALUES ($1) RETURNING id",
                    request.user_id
                )
            logger.info(f"Created new session: {session_id}")
        
        # Retrieve conversation history if session exists
        conversation_history = []
        if session_id:
            async with get_connection() as conn:
                rows = await conn.fetch(
                    """
                    SELECT role, content 
                    FROM chat_messages 
                    WHERE session_id = $1 
                    ORDER BY created_at ASC 
                    LIMIT 10
                    """,
                    session_id
                )
                conversation_history = [
                    {"role": row['role'], "content": row['content']}
                    for row in rows
                ]
        
        # Save user message
        async with get_connection() as conn:
            await conn.execute(
                """
                INSERT INTO chat_messages (session_id, role, content, selected_text)
                VALUES ($1, $2, $3, $4)
                """,
                session_id,
                "user",
                request.message,
                request.selected_text,
            )
        
        # Generate response using RAG
        logger.debug("Calling RAG service...")
        rag_result = await rag_service.answer_question(
            question=request.message,
            selected_text=request.selected_text,
            chapter_slug=request.chapter_slug,
            conversation_history=conversation_history,
            top_k=5,
        )
        
        answer = rag_result['answer']
        sources = rag_result.get('sources', [])
        
        # Save assistant response with metadata as JSON string
        metadata = json.dumps({"sources": [s['chapter_slug'] for s in sources]})
        async with get_connection() as conn:
            await conn.execute(
                """
                INSERT INTO chat_messages (session_id, role, content, metadata)
                VALUES ($1, $2, $3, $4)
                """,
                session_id,
                "assistant",
                answer,
                metadata,
            )
        
        # Format sources for response
        source_slugs = list(set(s['chapter_slug'] for s in sources))
        
        logger.info(f"Chat response generated: {len(answer)} chars, {len(source_slugs)} sources")
        
        return ChatResponse(
            response=answer,
            session_id=session_id,
            sources=source_slugs,
        )
        
    except asyncpg.PostgresError as e:
        logger.error(f"Database error in chat: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Database error occurred. Please try again."
        )
    except Exception as e:
        logger.error(f"Error processing chat request: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request. Please try again."
        )


@router.get("/sessions/{session_id}")
async def get_session_history(session_id: int):
    """
    Retrieve chat history for a session.
    
    Args:
        session_id: Session ID
        
    Returns:
        List of messages in the session
    """
    try:
        async with get_connection() as conn:
            # Check if session exists
            session = await conn.fetchrow(
                "SELECT id, user_id, created_at FROM chat_sessions WHERE id = $1",
                session_id
            )
            
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            
            # Get messages
            messages = await conn.fetch(
                """
                SELECT role, content, selected_text, created_at
                FROM chat_messages
                WHERE session_id = $1
                ORDER BY created_at ASC
                """,
                session_id
            )
            
            return {
                "session_id": session_id,
                "user_id": session['user_id'],
                "created_at": session['created_at'].isoformat(),
                "messages": [
                    {
                        "role": msg['role'],
                        "content": msg['content'],
                        "selected_text": msg['selected_text'],
                        "created_at": msg['created_at'].isoformat(),
                    }
                    for msg in messages
                ],
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving session: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve session")


@router.post("/search")
async def search_content(
    query: str,
    limit: int = 10,
    module_filter: Optional[str] = None,
    rag_service: RAGService = Depends(get_rag_service),
):
    """
    Search textbook content without generating a response.
    
    Useful for autocomplete, finding related topics, or direct search.
    
    Args:
        query: Search query
        limit: Maximum results (default 10)
        module_filter: Optional module name filter
        rag_service: RAG service dependency
        
    Returns:
        List of matching content chunks
    """
    try:
        results = await rag_service.search_textbook(
            query=query,
            limit=limit,
            module_filter=module_filter,
        )
        
        return {
            "query": query,
            "results": results,
            "count": len(results),
        }
    except Exception as e:
        logger.error(f"Search error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Search failed")


@router.get("/health")
async def health_check():
    """Check if chat service is healthy."""
    return {"status": "healthy", "service": "chat"}
