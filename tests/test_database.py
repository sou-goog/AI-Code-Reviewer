import pytest
from src.database import ReviewDatabase
import os
import tempfile

def test_database_initialization():
    """Test database initialization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, 'test.db')
        db = ReviewDatabase(db_path)
        
        assert os.path.exists(db_path)
        assert db.get_total_reviews() == 0

def test_save_review():
    """Test saving a review to database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, 'test.db')
        db = ReviewDatabase(db_path)
        
        review_data = {
            'diff_type': 'staged',
            'file_count': 2,
            'critical_count': 1,
            'warning_count': 3,
            'suggestion_count': 5,
            'review_text': 'Test review',
            'duration_seconds': 2.5
        }
        
        review_id = db.save_review(review_data)
        assert review_id > 0
        assert db.get_total_reviews() == 1

def test_get_review_stats():
    """Test getting review statistics."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, 'test.db')
        db = ReviewDatabase(db_path)
        
        # Add multiple reviews
        for i in range(3):
            db.save_review({
                'diff_type': 'staged',
                'file_count': i + 1,
                'critical_count': i,
                'warning_count': i * 2,
                'suggestion_count': i * 3,
                'review_text': f'Review {i}',
                'duration_seconds': float(i + 1)
            })
        
        stats = db.get_review_stats()
        
        assert stats['total_reviews'] == 3
        assert stats['total_issues']['critical'] == 3  # 0 + 1 + 2
        assert stats['total_issues']['warning'] == 6    # 0 + 2 + 4
        assert stats['total_issues']['suggestion'] == 9  # 0 + 3 + 6
