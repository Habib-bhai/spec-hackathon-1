"""
Google Gemini AI service for embeddings and chat.

This module provides wrappers for Google's Gemini API,
handling embeddings generation and chat completions.
"""

import os
import logging
import asyncio
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, TooManyRequests

logger = logging.getLogger(__name__)


class GeminiService:
    """
    Service for Google Gemini AI operations.
    
    Handles:
    - Text embeddings for semantic search
    - Chat completions with context
    - Rate limiting and error handling
    """
    
    def __init__(self):
        """Initialize Gemini client with API key from environment."""
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable is not set")
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Model names from environment or defaults
        # Free tier models and quotas (from Gemini API docs):
        # - gemini-2.5-flash: RPM 10, TPM 250K, RPD 250 ✅ (RECOMMENDED)
        # - gemini-2.0-flash: RPM 15, TPM 1M, RPD 200 ✅
        # - gemini-2.5-pro: RPM 2, TPM 125K, RPD 50 ✅
        # PAID ONLY (not in free tier):
        # - gemini-2.0-flash-lite: Tier 2/3 only ❌
        # - gemini-2.5-flash-lite: Tier 3 only ❌
        self.embedding_model_name = os.getenv("GEMINI_EMBEDDING_MODEL", "text-embedding-004")
        self.chat_model_name = os.getenv("GEMINI_CHAT_MODEL", "gemini-2.5-flash")
        
        # Initialize chat model only (embeddings use direct API call)
        # Note: text-embedding-004 is NOT a GenerativeModel, it's accessed via embed_content()
        self.chat_model = genai.GenerativeModel(self.chat_model_name)
        
        logger.info(
            f"Initialized GeminiService: "
            f"embedding={self.embedding_model_name}, chat={self.chat_model_name}"
        )
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for a single text.
        
        Args:
            text: Input text to embed
        
        Returns:
            List of floats representing the embedding vector (768 dimensions for text-embedding-004)
        
        Raises:
            ResourceExhausted: If Gemini API quota is exceeded
            TooManyRequests: If rate limit is hit
            Exception: For other API failures
        """
        try:
            # Run synchronous Gemini call in thread pool to avoid blocking event loop
            result = await asyncio.to_thread(
                genai.embed_content,
                model=f"models/{self.embedding_model_name}",
                content=text,
                task_type="retrieval_document",
            )
            
            embedding = result["embedding"]
            logger.debug(f"Generated embedding of dimension {len(embedding)}")
            return embedding
        
        except ResourceExhausted as e:
            logger.error(
                f"Gemini API quota exceeded. Free tier limit: 1500 requests/day. Error: {e}"
            )
            raise Exception(
                "AI service quota exceeded. Please try again later or contact support."
            ) from e
        
        except TooManyRequests as e:
            logger.warning(
                f"Gemini API rate limit hit. Free tier: 15 requests/minute. Error: {e}"
            )
            raise Exception(
                "Too many requests. Please wait a moment and try again."
            ) from e
            
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise Exception(
                "Failed to process your request. Please try again."
            ) from e
    
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch.
        
        Args:
            texts: List of input texts to embed
        
        Returns:
            List of embedding vectors
        
        Raises:
            Exception: If API call fails
        """
        if not texts:
            return []
        
        try:
            # Process in chunks to avoid rate limits
            # Gemini free tier: 1500 requests/day, but batch is more efficient
            embeddings = []
            
            for text in texts:
                embedding = await self.generate_embedding(text)
                embeddings.append(embedding)
            
            logger.info(f"Generated {len(embeddings)} embeddings")
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {e}")
            raise
    
    async def generate_chat_response(
        self,
        query: str,
        context_chunks: List[str],
        conversation_history: Optional[List[Dict[str, str]]] = None,
        selected_text: Optional[str] = None,
    ) -> str:
        """
        Generate a chat response using RAG (Retrieval-Augmented Generation).
        
        Args:
            query: User's question
            context_chunks: Retrieved relevant text chunks from the textbook
            conversation_history: Previous messages in the conversation
            selected_text: Text selected by user for additional context
        
        Returns:
            Generated response text
        
        Raises:
            ResourceExhausted: If Gemini API quota is exceeded
            TooManyRequests: If rate limit is hit
            Exception: For other API failures
        """
        try:
            # Build the prompt with context
            system_prompt = (
                "You are a helpful AI tutor for a Physical AI textbook. "
                "Your role is to explain concepts clearly, provide practical examples, "
                "and help students understand robotics and AI topics. "
                "Use the provided context from the textbook to answer questions accurately. "
                "If you're not sure about something, say so."
            )
            
            # Add retrieved context
            context_text = "\n\n".join(
                f"[Context {i+1}]:\n{chunk}"
                for i, chunk in enumerate(context_chunks)
            )
            
            prompt_parts = [system_prompt]
            
            if context_text:
                prompt_parts.append(f"\n\nRelevant textbook content:\n{context_text}")
            
            if selected_text:
                prompt_parts.append(f"\n\nUser selected this text for context:\n\"{selected_text}\"")
            
            # Add conversation history if available
            if conversation_history:
                history_text = "\n".join(
                    f"{msg['role'].capitalize()}: {msg['content']}"
                    for msg in conversation_history[-5:]  # Last 5 messages
                )
                prompt_parts.append(f"\n\nConversation history:\n{history_text}")
            
            # Add the current query
            prompt_parts.append(f"\n\nStudent question: {query}")
            
            full_prompt = "\n".join(prompt_parts)
            
            # Run synchronous Gemini call in thread pool to avoid blocking event loop
            response = await asyncio.to_thread(
                self.chat_model.generate_content,
                full_prompt
            )
            
            response_text = response.text
            logger.info(f"Generated chat response ({len(response_text)} chars)")
            return response_text
        
        except ResourceExhausted as e:
            logger.error(
                f"Gemini API quota exceeded for chat completion. Error: {e}"
            )
            raise Exception(
                "AI service quota exceeded. Please try again later."
            ) from e
        
        except TooManyRequests as e:
            logger.warning(
                f"Gemini API rate limit hit for chat completion. Error: {e}"
            )
            raise Exception(
                "Too many requests. Please wait a moment and try again."
            ) from e
            
        except Exception as e:
            logger.error(f"Failed to generate chat response: {e}")
            raise Exception(
                "Failed to generate response. Please try again."
            ) from e
    
    async def translate_text(self, text: str, target_language: str) -> str:
        """
        Translate text to target language using Gemini.
        
        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'es', 'zh', 'fr')
        
        Returns:
            Translated text
        
        Raises:
            Exception: If API call fails
        """
        try:
            prompt = (
                f"Translate the following technical/educational content to {target_language}. "
                f"Maintain technical terms and formatting:\n\n{text}"
            )
            
            response = self.chat_model.generate_content(prompt)
            translated = response.text
            
            logger.info(f"Translated text to {target_language} ({len(translated)} chars)")
            return translated
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            raise
