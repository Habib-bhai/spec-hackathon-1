"""Quick test script to debug RAG pipeline issues."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from api.services.gemini_service import GeminiService
from api.services.vector_service import VectorService
from api.services.rag_service import RAGService


async def test_rag():
    """Test the RAG pipeline step by step."""
    print("🔍 Testing RAG Pipeline...\n")
    
    # Step 1: Test Gemini Service
    print("1️⃣ Testing Gemini Service...")
    gemini = GeminiService()
    try:
        embedding = await gemini.generate_embedding("test query")
        print(f"   ✅ Embedding generated: {len(embedding)} dimensions\n")
    except Exception as e:
        print(f"   ❌ Embedding failed: {e}\n")
        return
    
    # Step 2: Test Vector Service
    print("2️⃣ Testing Vector Service...")
    vector_service = VectorService()
    try:
        # Check collection info
        collections = await vector_service.client.get_collections()
        print(f"   📚 Collections: {[c.name for c in collections.collections]}")
        
        # Try to get collection info
        info = await vector_service.client.get_collection(vector_service.collection_name)
        print(f"   📊 Collection '{vector_service.collection_name}': {info.points_count} points")
        
        if info.points_count == 0:
            print(f"   ⚠️  Collection is empty! Run: python scripts/index_content.py\n")
            return
        
        # Try a search
        results = await vector_service.search(
            query_vector=embedding,
            limit=3
        )
        print(f"   ✅ Search successful: {len(results)} results\n")
        for i, r in enumerate(results, 1):
            print(f"      {i}. Score: {r['score']:.4f}, Chapter: {r['payload'].get('chapter_slug', 'N/A')}")
        print()
        
    except Exception as e:
        print(f"   ❌ Vector search failed: {e}\n")
        import traceback
        traceback.print_exc()
        return
    
    # Step 3: Test RAG Service
    print("3️⃣ Testing RAG Service...")
    rag_service = RAGService(gemini_service=gemini, vector_service=vector_service)
    try:
        result = await rag_service.answer_question(
            question="What is ROS 2?",
            conversation_history=[],
            top_k=3
        )
        print(f"   ✅ RAG answer generated:")
        print(f"      Answer: {result['answer'][:200]}...")
        print(f"      Sources: {len(result['sources'])} chunks\n")
        
    except Exception as e:
        print(f"   ❌ RAG failed: {e}\n")
        import traceback
        traceback.print_exc()
        return
    
    print("✨ All tests passed!")


if __name__ == "__main__":
    asyncio.run(test_rag())
