"""
RAG (Retrieval-Augmented Generation) service for chatbot.

This service combines vector search with LLM generation to answer
questions about textbook content with grounded, contextual responses.
"""

import logging
from typing import List, Dict, Any, Optional

from api.services.vector_service import VectorService
from api.services.gemini_service import GeminiService

logger = logging.getLogger(__name__)


class RAGService:
    """
    Service for Retrieval-Augmented Generation chatbot.
    
    Combines semantic search over textbook content with Gemini LLM
    to provide accurate, grounded answers to student questions.
    """
    
    def __init__(
        self,
        vector_service: VectorService,
        gemini_service: GeminiService,
    ):
        """
        Initialize RAG service.
        
        Args:
            vector_service: Vector database service
            gemini_service: Gemini AI service
        """
        self.vector_service = vector_service
        self.gemini_service = gemini_service
        logger.info("Initialized RAG service")
    
    async def answer_question(
        self,
        question: str,
        selected_text: Optional[str] = None,
        chapter_slug: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """
        Answer a question using RAG.
        
        Args:
            question: User's question
            selected_text: Text selected by user for additional context
            chapter_slug: Current chapter slug for scoped search
            conversation_history: Previous messages for context
            top_k: Number of context chunks to retrieve
            
        Returns:
            Dict with:
                - answer: Generated response text
                - sources: List of source chunks used
                - context_chunks: Retrieved context texts
        """
        logger.info(f"Answering question: {question[:100]}...")
        
        try:
            # Step 1: Generate embedding for the question
            logger.debug("Generating question embedding...")
            question_embedding = await self.gemini_service.generate_embedding(question)
            
            # Step 2: Search for relevant context
            logger.debug(f"Searching for top {top_k} relevant chunks...")
            search_results = await self.vector_service.search(
                query_vector=question_embedding,
                limit=top_k,
                chapter_slug=chapter_slug,
            )
            
            if not search_results:
                logger.warning("No relevant context found")
                return {
                    "answer": (
                        "I couldn't find relevant information in the textbook to answer your question. "
                        "Could you try rephrasing or asking about a different topic?"
                    ),
                    "sources": [],
                    "context_chunks": [],
                }
            
            # Step 3: Extract context chunks and metadata
            context_chunks = []
            sources = []
            
            for result in search_results:
                payload = result['payload']
                context_chunks.append(payload['content'])
                
                # Track unique source chapters
                source_info = {
                    'chapter_slug': payload['chapter_slug'],
                    'module_name': payload.get('module_name', 'unknown'),
                    'score': result['score'],
                }
                if source_info not in sources:
                    sources.append(source_info)
            
            logger.info(f"Retrieved {len(context_chunks)} chunks from {len(sources)} sources")
            
            # Step 4: Generate answer using Gemini with context
            logger.debug("Generating answer with LLM...")
            answer = await self.gemini_service.generate_chat_response(
                query=question,
                context_chunks=context_chunks,
                conversation_history=conversation_history,
                selected_text=selected_text,
            )
            
            logger.info(f"Generated answer: {len(answer)} characters")
            
            return {
                "answer": answer,
                "sources": sources,
                "context_chunks": context_chunks,
            }
            
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {e}", exc_info=True)
            return {
                "answer": (
                    "I encountered an error while processing your question. "
                    "Please try again or rephrase your question."
                ),
                "sources": [],
                "context_chunks": [],
                "error": str(e),
            }
    
    async def get_similar_content(
        self,
        text: str,
        limit: int = 3,
        chapter_slug: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find similar content in the textbook.
        
        Useful for "related topics" or "see also" features.
        
        Args:
            text: Text to find similar content for
            limit: Number of results to return
            chapter_slug: Optional chapter filter
            
        Returns:
            List of similar chunks with metadata
        """
        try:
            # Generate embedding
            embedding = await self.gemini_service.generate_embedding(text)
            
            # Search
            results = await self.vector_service.search(
                query_vector=embedding,
                limit=limit,
                chapter_slug=chapter_slug,
            )
            
            # Format results
            similar = [
                {
                    'content': result['payload']['content'],
                    'chapter_slug': result['payload']['chapter_slug'],
                    'module_name': result['payload'].get('module_name'),
                    'score': result['score'],
                }
                for result in results
            ]
            
            return similar
            
        except Exception as e:
            logger.error(f"Error finding similar content: {e}")
            return []
    
    async def search_textbook(
        self,
        query: str,
        limit: int = 10,
        module_filter: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search textbook content directly (without generating an answer).
        
        Args:
            query: Search query
            limit: Maximum results
            module_filter: Optional module name filter
            
        Returns:
            List of matching chunks with metadata
        """
        try:
            # Generate embedding
            embedding = await self.gemini_service.generate_embedding(query)
            
            # Search
            results = await self.vector_service.search(
                query_vector=embedding,
                limit=limit,
                module_name=module_filter,
            )
            
            # Format results
            formatted = [
                {
                    'content': result['payload']['content'],
                    'chapter_slug': result['payload']['chapter_slug'],
                    'module_name': result['payload'].get('module_name'),
                    'chunk_index': result['payload'].get('chunk_index', 0),
                    'score': result['score'],
                }
                for result in results
            ]
            
            logger.info(f"Search found {len(formatted)} results for: {query}")
            return formatted
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
