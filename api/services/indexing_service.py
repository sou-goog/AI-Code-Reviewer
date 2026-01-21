"""
Repository Indexing Service
Indexes entire repositories by generating embeddings for all code files
"""
import os
from typing import Dict, List
from github import Github
from .embedding_service import EmbeddingService

class IndexingService:
    """Index repository codebase for RAG"""
    
    # Supported code file extensions
    CODE_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx',
        '.java', '.cpp', '.c', '.h', '.hpp',
        '.go', '.rs', '.rb', '.php',
        '.cs', '.swift', '.kt', '.scala',
        '.sql', '.sh', '.bash',
        '.html', '.css', '.scss', '.sass',
        '.json', '.yaml', '.yml', '.toml',
        '.md', '.txt'
    }
    
    # Files to skip
    SKIP_PATTERNS = {
        'node_modules', 'venv', '__pycache__', '.git',
        'dist', 'build', 'target', '.next',
        'package-lock.json', 'yarn.lock', 'poetry.lock'
    }
    
    def __init__(self):
        """Initialize indexing service"""
        self.embedding_service = EmbeddingService()
    
    async def index_repository(
        self, 
        repo_full_name: str, 
        repo_id: str,
        github_token: str
    ) -> Dict:
        """
        Index all code files in a repository
        
        Args:
            repo_full_name: Repository name (owner/repo)
            repo_id: Internal repository ID
            github_token: GitHub access token
            
        Returns:
            Dict with indexing statistics
        """
        stats = {
            "total_files": 0,
            "indexed_files": 0,
            "skipped_files": 0,
            "errors": 0
        }
        
        try:
            # Initialize GitHub client
            g = Github(github_token)
            repo = g.get_repo(repo_full_name)
            
            # Get all files from the repository
            contents = repo.get_contents("")
            
            while contents:
                file_content = contents.pop(0)
                
                if file_content.type == "dir":
                    # Skip certain directories
                    if any(pattern in file_content.path for pattern in self.SKIP_PATTERNS):
                        continue
                    # Add directory contents to queue
                    contents.extend(repo.get_contents(file_content.path))
                else:
                    stats["total_files"] += 1
                    
                    # Check if it's a code file
                    if not self._is_code_file(file_content.path):
                        stats["skipped_files"] += 1
                        continue
                    
                    # Index the file
                    success = await self._index_file(
                        file_content, 
                        repo_id,
                        repo_full_name
                    )
                    
                    if success:
                        stats["indexed_files"] += 1
                    else:
                        stats["errors"] += 1
            
            return stats
        except Exception as e:
            print(f"Error indexing repository: {e}")
            stats["errors"] += 1
            return stats
    
    async def _index_file(
        self, 
        file_content, 
        repo_id: str,
        repo_full_name: str
    ) -> bool:
        """
        Index a single file
        
        Args:
            file_content: GitHub file content object
            repo_id: Repository ID
            repo_full_name: Repository full name
            
        Returns:
            True if successful
        """
        try:
            # Get file content (limit size to 1MB)
            if file_content.size > 1_000_000:
                print(f"Skipping large file: {file_content.path}")
                return False
            
            # Decode content
            try:
                code = file_content.decoded_content.decode('utf-8')
            except UnicodeDecodeError:
                print(f"Skipping binary file: {file_content.path}")
                return False
            
            # Prepare metadata
            metadata = {
                "repo_name": repo_full_name,
                "file_size": file_content.size,
                "sha": file_content.sha
            }
            
            # Store embedding
            success = await self.embedding_service.store_code_embedding(
                file_path=file_content.path,
                code_content=code,
                repo_id=repo_id,
                metadata=metadata
            )
            
            return success
        except Exception as e:
            print(f"Error indexing file {file_content.path}: {e}")
            return False
    
    def _is_code_file(self, file_path: str) -> bool:
        """Check if file is a code file based on extension"""
        extension = os.path.splitext(file_path)[1].lower()
        return extension in self.CODE_EXTENSIONS
    
    async def reindex_repository(
        self, 
        repo_full_name: str, 
        repo_id: str,
        github_token: str
    ) -> Dict:
        """
        Reindex a repository (delete old embeddings and create new ones)
        
        Args:
            repo_full_name: Repository name (owner/repo)
            repo_id: Internal repository ID  
            github_token: GitHub access token
            
        Returns:
            Dict with indexing statistics
        """
        # Delete existing embeddings
        await self.embedding_service.delete_repo_embeddings(repo_id)
        
        # Index repository
        return await self.index_repository(repo_full_name, repo_id, github_token)
