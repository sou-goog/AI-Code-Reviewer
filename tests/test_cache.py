"""
Tests for caching system.
"""
import pytest
import tempfile
from pathlib import Path
from src.utils.cache import ReviewCache


def test_cache_initialization():
    """Test cache initializes with custom directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = ReviewCache(cache_dir=Path(tmpdir))
        assert cache.cache_dir.exists()


def test_cache_get_set():
    """Test basic cache get/set operations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = ReviewCache(cache_dir=Path(tmpdir))
        
        # Set cache
        review_data = {"review": "Test review", "model": "gemini-2.5-flash"}
        cache.set("test_key", review_data)
        
        # Get cache
        result = cache.get("test_key")
        assert result is not None
        assert result["review"] == "Test review"


def test_cache_miss():
    """Test cache miss returns None."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = ReviewCache(cache_dir=Path(tmpdir))
        result = cache.get("nonexistent_key")
        assert result is None


def test_cache_expiry():
    """Test cache entries expire after TTL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create cache with 0-day TTL (expires immediately)
        cache = ReviewCache(cache_dir=Path(tmpdir), ttl_days=0)
        
        review_data = {"review": "Test review"}
        cache.set("test_key", review_data)
        
        # Should be expired immediately
        result = cache.get("test_key")
        assert result is None


def test_cache_key_generation():
    """Test cache key is deterministic."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = ReviewCache(cache_dir=Path(tmpdir))
        
        key1 = cache.get_cache_key("diff content", "gemini-2.5-flash")
        key2 = cache.get_cache_key("diff content", "gemini-2.5-flash")
        
        assert key1 == key2
        
        # Different content should have different key
        key3 = cache.get_cache_key("other content", "gemini-2.5-flash")
        assert key1 != key3


def test_cache_stats():
    """Test cache statistics."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = ReviewCache(cache_dir=Path(tmpdir))
        
        # Empty cache
        stats = cache.get_stats()
        assert stats["count"] == 0
        
        # Add some entries
        for i in range(3):
            cache.set(f"key_{i}", {"review": f"Review {i}"})
        
        stats = cache.get_stats()
        assert stats["count"] == 3
        assert stats["total_size_mb"] > 0
