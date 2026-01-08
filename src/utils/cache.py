"""
File-based caching system for review results.
"""
import hashlib
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ReviewCache:
    """
    File-based cache for review results to avoid re-reviewing identical code.
    
    Cache keys are based on hash of diff content and model name.
    Cached entries expire after 7 days.
    """
    
    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        ttl_days: int = 7
    ):
        """
        Initialize cache.
        
        Args:
            cache_dir: Directory for cache files (default: ~/.code-reviewer/cache)
            ttl_days: Time-to-live for cache entries in days
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".code-reviewer" / "cache"
        
        self.cache_dir = Path(cache_dir)
        self.ttl_seconds = ttl_days * 86400
        
        # Create cache directory if it doesn't exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized cache at {self.cache_dir}")
    
    def get_cache_key(self, code_diff: str, model: str) -> str:
        """
        Generate unique cache key for code diff and model.
        
        Args:
            code_diff: Git diff string
            model: AI model name
            
        Returns:
            SHA256 hash as cache key
        """
        content = f"{code_diff}:{model}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached review if exists and not expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached review dict or None if not found/expired
        """
        cache_file = self.cache_dir / f"{key}.json"
        
        if not cache_file.exists():
            logger.debug(f"Cache miss: {key}")
            return None
        
        # Check if cache is still fresh
        age_seconds = time.time() - cache_file.stat().st_mtime
        
        if age_seconds > self.ttl_seconds:
            logger.debug(f"Cache expired: {key} (age: {age_seconds/86400:.1f} days)")
            # Delete expired cache
            cache_file.unlink()
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"Cache hit: {key} (age: {age_seconds/3600:.1f} hours)")
            return data
            
        except Exception as e:
            logger.warning(f"Error reading cache {key}: {e}")
            return None
    
    def set(self, key: str, review: Dict[str, Any]) -> None:
        """
        Store review in cache.
        
        Args:
            key: Cache key
            review: Review data to cache
        """
        cache_file = self.cache_dir / f"{key}.json"
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(review, f, indent=2)
            
            logger.debug(f"Cached review: {key}")
            
        except Exception as e:
            logger.warning(f"Error writing cache {key}: {e}")
    
    def clear_old_entries(self, max_age_days: Optional[int] = None) -> int:
        """
        Remove old cache entries.
        
        Args:
            max_age_days: Maximum age in days (default: uses TTL)
            
        Returns:
            Number of entries removed
        """
        if max_age_days is None:
            max_age_seconds = self.ttl_seconds
        else:
            max_age_seconds = max_age_days * 86400
        
        removed = 0
        now = time.time()
        
        for cache_file in self.cache_dir.glob("*.json"):
            age = now - cache_file.stat().st_mtime
            if age > max_age_seconds:
                cache_file.unlink()
                removed += 1
        
        if removed > 0:
            logger.info(f"Removed {removed} old cache entries")
        
        return removed
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dict with cache stats (count, total size, oldest entry)
        """
        cache_files = list(self.cache_dir.glob("*.json"))
        
        if not cache_files:
            return {
                "count": 0,
                "total_size_mb": 0,
                "oldest_age_days": 0
            }
        
        total_size = sum(f.stat().st_size for f in cache_files)
        oldest = min(f.stat().st_mtime for f in cache_files)
        oldest_age = (time.time() - oldest) / 86400
        
        return {
            "count": len(cache_files),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "oldest_age_days": round(oldest_age, 1)
        }
