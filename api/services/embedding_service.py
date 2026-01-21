"""
Embedding Service for RAG Implementation
Generates vector embeddings for code using Google's text-embedding-004 model
"""
import os
from typing import List, Dict, Optional
import google.generativeai as genai
from pinecone import Pinecone, ServerlessSpec
import hashlib

class EmbeddingService:
    """Generate and manage code embeddings for RAG"""
    
    def __init__(self):
        """Initialize Pinecone and Gemini clients"""
        # Initialize Pinecone
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "code-reviewer")
        
        # Get or create index
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=768,  # text-embedding-004 dimension
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region=os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
                )
            )
        
        self.index = self.pc.Index(self.index_name)
        
        # Configure Gemini for embeddings
        genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))
    
    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for text using Google's text-embedding-004
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
    
    async def store_code_embedding(
        self, 
        file_path: str, 
        code_content: str, 
        repo_id: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Generate and store embedding for a code file
        
        Args:
            file_path: Path of the file in repository
            code_content: Content of the code file
            repo_id: Repository identifier
            metadata: Additional metadata to store
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Generate unique ID for this code chunk
            chunk_id = hashlib.md5(f"{repo_id}:{file_path}".encode()).hexdigest()
            
            # Generate embedding
            embedding = await self.embed_text(code_content)
            
            if not embedding:
                return False
            
            # Prepare metadata
            vector_metadata = {
                "repo_id": repo_id,
                "file_path": file_path,
                "code_preview": code_content[:200],  # First 200 chars for preview
                "file_type": file_path.split('.')[-1] if '.' in file_path else 'unknown',
                **(metadata or {})
            }
            
            # Store in Pinecone
            self.index.upsert(vectors=[(chunk_id, embedding, vector_metadata)])
            
            return True
        except Exception as e:
            print(f"Error storing embedding: {e}")
            return False
    
    async def search_similar_code(
        self, 
        query: str, 
        repo_id: str, 
        top_k: int = 5
    ) -> List[Dict]:
        """
        Search for similar code snippets using semantic search
        
        Args:
            query: Search query (e.g., PR diff or description)
            repo_id: Repository to search within
            top_k: Number of results to return
            
        Returns:
            List of matching code snippets with metadata
        """
        try:
            # Generate embedding for query
            query_embedding = await self.embed_text(query)
            
            if not query_embedding:
                return []
            
            # Search in Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                filter={"repo_id": repo_id},
                include_metadata=True
            )
            
            # Format results
            matches = []
            for match in results.get('matches', []):
                matches.append({
                    "file_path": match['metadata'].get('file_path'),
                    "code_preview": match['metadata'].get('code_preview'),
                    "similarity_score": match['score'],
                    "file_type": match['metadata'].get('file_type')
                })
            
            return matches
        except Exception as e:
            print(f"Error searching similar code: {e}")
            return []
    
    async def delete_repo_embeddings(self, repo_id: str) -> bool:
        """
        Delete all embeddings for a repository
        
        Args:
            repo_id: Repository identifier
            
        Returns:
            True if successful
        """
        try:
            # Delete by metadata filter
            self.index.delete(filter={"repo_id": repo_id})
            return True
        except Exception as e:
            print(f"Error deleting embeddings: {e}")
            return False
    
    def get_index_stats(self) -> Dict:
        """Get statistics about the Pinecone index"""
        try:
            return self.index.describe_index_stats()
        except Exception as e:
            print(f"Error getting index stats: {e}")
            return {}
