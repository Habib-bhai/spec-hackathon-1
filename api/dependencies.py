"""
Dependency injection functions for FastAPI endpoints.

This module provides dependency functions that can be used
across routers without creating circular imports.
"""

from typing import Optional
from api.services import VectorService, GeminiService, RAGService

# Global service instances (initialized in main.py lifespan)
_vector_service: Optional[VectorService] = None


def set_vector_service(service: VectorService) -> None:
    """
    Set the global vector service instance.
    
    Called during application startup.
    
    Args:
        service: The initialized vector service
    """
    global _vector_service
    _vector_service = service


def get_vector_service() -> VectorService:
    """
    Dependency to get the global vector service instance.
    
    Returns:
        VectorService: The initialized vector service
        
    Raises:
        RuntimeError: If vector service is not initialized
    """
    if _vector_service is None:
        raise RuntimeError("Vector service not initialized")
    return _vector_service


def get_rag_service() -> RAGService:
    """
    Dependency to get RAG service instance.
    
    Returns:
        RAGService: The initialized RAG service
        
    Raises:
        RuntimeError: If vector service is not initialized
    """
    vector_service = get_vector_service()
    gemini_service = GeminiService()
    return RAGService(vector_service, gemini_service)
