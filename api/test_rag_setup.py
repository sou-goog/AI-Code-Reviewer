"""
Test script to verify Pinecone connection and RAG setup
Run this to ensure everything is configured correctly
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.embedding_service import EmbeddingService

async def test_pinecone_connection():
    """Test Pinecone connection and embedding generation"""
    print("🧪 Testing Pinecone RAG Setup...")
    print("=" * 50)
    
    try:
        # Initialize embedding service
        print("\n1️⃣  Initializing Embedding Service...")
        service = EmbeddingService()
        print("✅ Embedding service initialized successfully!")
        
        # Test embedding generation
        print("\n2️⃣  Testing embedding generation...")
        test_code = """
def hello_world():
    print("Hello, World!")
    return True
"""
        embedding = await service.embed_text(test_code)
        print(f"✅ Generated embedding with {len(embedding)} dimensions")
        
        # Test storing embedding
        print("\n3️⃣  Testing embedding storage...")
        success = await service.store_code_embedding(
            file_path="test/hello.py",
            code_content=test_code,
            repo_id="test_repo_123",
            metadata={"test": True}
        )
        
        if success:
            print("✅ Successfully stored embedding in Pinecone!")
        else:
            print("❌ Failed to store embedding")
            return False
        
        # Test semantic search
        print("\n4️⃣  Testing semantic search...")
        results = await service.search_similar_code(
            query="function that prints hello world",
            repo_id="test_repo_123",
            top_k=1
        )
        
        if results:
            print(f"✅ Found {len(results)} similar code snippet(s)!")
            print(f"   - File: {results[0]['file_path']}")
            print(f"   - Similarity: {results[0]['similarity_score']:.4f}")
        else:
            print("❌ No results found")
            return False
        
        # Get index stats
        print("\n5️⃣  Checking index statistics...")
        stats = service.get_index_stats()
        print(f"✅ Index stats: {stats}")
        
        # Cleanup test data
        print("\n6️⃣  Cleaning up test data...")
        await service.delete_repo_embeddings("test_repo_123")
        print("✅ Test data cleaned up!")
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! RAG is ready to use!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        print(f"   Type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_pinecone_connection())
    sys.exit(0 if success else 1)
