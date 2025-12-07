"""
Content indexing script for Physical AI Textbook.

This script:
1. Parses MDX chapter files from book/docs/
2. Extracts text content (strips MDX/JSX)
3. Chunks content into semantic pieces
4. Generates embeddings using Gemini
5. Upserts chunks to Qdrant vector database

Usage:
    python scripts/index_content.py [--force-recreate] [--batch-size 10]
"""

import asyncio
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any
import argparse

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from api.services.vector_service import VectorService
from api.services.gemini_service import GeminiService

load_dotenv()


class MDXParser:
    """Parse MDX files and extract text content."""
    
    @staticmethod
    def parse_file(file_path: Path) -> Dict[str, Any]:
        """
        Parse an MDX file and extract metadata and content.
        
        Args:
            file_path: Path to the MDX file
            
        Returns:
            Dict with 'metadata' (frontmatter) and 'content' (text)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract frontmatter (YAML between --- markers)
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        metadata = {}
        text_content = content
        
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            text_content = content[frontmatter_match.end():]
            
            # Parse simple YAML frontmatter
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
        
        # Clean MDX/JSX content
        cleaned_content = MDXParser.clean_mdx(text_content)
        
        return {
            'metadata': metadata,
            'content': cleaned_content,
            'raw_content': content,
        }
    
    @staticmethod
    def clean_mdx(content: str) -> str:
        """
        Remove MDX/JSX syntax and extract plain text.
        
        Args:
            content: Raw MDX content
            
        Returns:
            Cleaned plain text
        """
        # Remove JSX components (e.g., <Component prop="value">)
        content = re.sub(r'<[A-Z][^>]*>', '', content)
        content = re.sub(r'</[A-Z][^>]*>', '', content)
        
        # Remove import statements
        content = re.sub(r'^import\s+.*?from\s+[\'"].*?[\'"];?\s*$', '', content, flags=re.MULTILINE)
        
        # Remove export statements
        content = re.sub(r'^export\s+.*?$', '', content, flags=re.MULTILINE)
        
        # Remove HTML comments
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        
        # Convert code blocks to plain text (keep the content)
        content = re.sub(r'```[\w]*\n(.*?)```', r'\1', content, flags=re.DOTALL)
        
        # Remove inline code formatting but keep text
        content = re.sub(r'`([^`]+)`', r'\1', content)
        
        # Remove Markdown links but keep text
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
        
        # Remove image syntax
        content = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', content)
        
        # Remove bold/italic markers
        content = re.sub(r'\*\*([^\*]+)\*\*', r'\1', content)
        content = re.sub(r'\*([^\*]+)\*', r'\1', content)
        content = re.sub(r'__([^_]+)__', r'\1', content)
        content = re.sub(r'_([^_]+)_', r'\1', content)
        
        # Remove headers but keep text
        content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)
        
        # Remove multiple blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content.strip()


class ContentChunker:
    """Chunk content into semantic pieces for embedding."""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 100):
        """
        Initialize chunker.
        
        Args:
            chunk_size: Maximum words per chunk
            overlap: Number of words to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_by_section(self, content: str) -> List[str]:
        """
        Chunk content by markdown sections (headers).
        
        Args:
            content: Cleaned text content
            
        Returns:
            List of text chunks
        """
        # Split by double newlines (paragraphs)
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        chunks = []
        current_chunk = []
        current_word_count = 0
        
        for paragraph in paragraphs:
            word_count = len(paragraph.split())
            
            if current_word_count + word_count <= self.chunk_size:
                current_chunk.append(paragraph)
                current_word_count += word_count
            else:
                # Save current chunk
                if current_chunk:
                    chunks.append('\n\n'.join(current_chunk))
                
                # Start new chunk
                if word_count <= self.chunk_size:
                    current_chunk = [paragraph]
                    current_word_count = word_count
                else:
                    # Split large paragraph
                    words = paragraph.split()
                    for i in range(0, len(words), self.chunk_size - self.overlap):
                        chunk_words = words[i:i + self.chunk_size]
                        chunks.append(' '.join(chunk_words))
                    current_chunk = []
                    current_word_count = 0
        
        # Add final chunk
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
        
        return chunks


async def index_chapter(
    file_path: Path,
    vector_service: VectorService,
    gemini_service: GeminiService,
    chunker: ContentChunker,
    force_reindex: bool = False
) -> int:
    """
    Index a single chapter file.
    
    Args:
        file_path: Path to MDX file
        vector_service: Vector service instance
        gemini_service: Gemini service instance
        chunker: Content chunker
        force_reindex: If True, delete existing chunks first
        
    Returns:
        Number of chunks indexed
    """
    print(f"\n📄 Processing: {file_path.relative_to(file_path.parents[2])}")
    
    # Parse MDX file
    parsed = MDXParser.parse_file(file_path)
    content = parsed['content']
    
    if not content or len(content) < 50:
        print(f"  ⚠️  Skipping (content too short)")
        return 0
    
    # Generate chapter slug from file path
    relative_path = file_path.relative_to(file_path.parents[2])
    chapter_slug = str(relative_path).replace('\\', '/').replace('.mdx', '').replace('book/docs/', '')
    
    # Extract module name
    module_match = re.match(r'(module-\d+)-([^/]+)', chapter_slug)
    module_name = module_match.group(0) if module_match else 'unknown'
    
    print(f"  📌 Slug: {chapter_slug}")
    print(f"  📦 Module: {module_name}")
    
    # Delete existing chunks if force reindex
    if force_reindex:
        try:
            await vector_service.delete_by_chapter(chapter_slug)
            print(f"  🗑️  Deleted existing chunks")
        except Exception as e:
            print(f"  ⚠️  Could not delete existing chunks: {e}")
    
    # Chunk content
    chunks = chunker.chunk_by_section(content)
    print(f"  ✂️  Created {len(chunks)} chunks")
    
    if not chunks:
        return 0
    
    # Generate embeddings
    print(f"  🧠 Generating embeddings...")
    try:
        embeddings = await gemini_service.generate_embeddings_batch(chunks)
    except Exception as e:
        print(f"  ❌ Failed to generate embeddings: {e}")
        return 0
    
    # Prepare documents
    documents = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        documents.append({
            'chapter_slug': chapter_slug,
            'module_name': module_name,
            'chunk_index': i,
            'content': chunk,
            'word_count': len(chunk.split()),
        })
    
    # Upsert to Qdrant
    print(f"  💾 Upserting to Qdrant...")
    try:
        await vector_service.upsert_documents(documents, embeddings)
        print(f"  ✅ Indexed {len(chunks)} chunks")
        return len(chunks)
    except Exception as e:
        print(f"  ❌ Failed to upsert: {e}")
        return 0


async def index_all_chapters(
    docs_dir: Path,
    force_recreate: bool = False,
    batch_size: int = 10
) -> None:
    """
    Index all MDX chapters in the docs directory.
    
    Args:
        docs_dir: Path to book/docs/ directory
        force_recreate: If True, recreate Qdrant collection
        batch_size: Number of files to process in parallel
    """
    print("🚀 Starting content indexing for Physical AI Textbook\n")
    
    # Initialize services
    print("🔧 Initializing services...")
    vector_service = VectorService()
    gemini_service = GeminiService()
    chunker = ContentChunker(chunk_size=500, overlap=100)
    
    # Create or verify collection
    print("📊 Setting up Qdrant collection...")
    try:
        await vector_service.create_collection(vector_size=768, force_recreate=force_recreate)
        print("✅ Collection ready\n")
    except Exception as e:
        print(f"❌ Failed to setup collection: {e}")
        return
    
    # Find all MDX files
    mdx_files = list(docs_dir.rglob("*.mdx"))
    print(f"📚 Found {len(mdx_files)} MDX files\n")
    
    if not mdx_files:
        print("⚠️  No MDX files found. Check the docs directory path.")
        return
    
    # Index files
    total_chunks = 0
    for i, file_path in enumerate(mdx_files, 1):
        print(f"\n[{i}/{len(mdx_files)}]", end=' ')
        chunks = await index_chapter(
            file_path,
            vector_service,
            gemini_service,
            chunker,
            force_reindex=force_recreate
        )
        total_chunks += chunks
        
        # Small delay to avoid rate limits
        await asyncio.sleep(1)
    
    # Summary
    print("\n" + "="*60)
    print(f"✨ Indexing complete!")
    print(f"📊 Total files processed: {len(mdx_files)}")
    print(f"📦 Total chunks indexed: {total_chunks}")
    print(f"🎯 Average chunks per file: {total_chunks / len(mdx_files):.1f}")
    print("="*60)
    
    # Close connections
    await vector_service.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Index textbook content for RAG chatbot")
    parser.add_argument(
        '--force-recreate',
        action='store_true',
        help='Delete and recreate Qdrant collection (WARNING: deletes all existing data)'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=10,
        help='Number of files to process in parallel (default: 10)'
    )
    parser.add_argument(
        '--docs-dir',
        type=str,
        default='book/docs',
        help='Path to docs directory (default: book/docs)'
    )
    
    args = parser.parse_args()
    
    # Validate docs directory
    docs_dir = Path(args.docs_dir)
    if not docs_dir.exists():
        print(f"❌ Error: Docs directory not found: {docs_dir}")
        sys.exit(1)
    
    # Check environment variables
    required_env_vars = ['QDRANT_URL', 'GEMINI_API_KEY']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set them in your .env file")
        sys.exit(1)
    
    # Run indexing
    try:
        asyncio.run(index_all_chapters(
            docs_dir,
            force_recreate=args.force_recreate,
            batch_size=args.batch_size
        ))
    except KeyboardInterrupt:
        print("\n\n⚠️  Indexing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Indexing failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
