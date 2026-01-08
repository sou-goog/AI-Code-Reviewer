import pytest
from src.git_handler import get_staged_diff, get_uncommitted_diff

def test_get_staged_diff_no_repo(tmp_path):
    """Test that get_staged_diff returns None for non-git directory."""
    result = get_staged_diff(str(tmp_path))
    assert result is None

def test_get_uncommitted_diff_no_repo(tmp_path):
    """Test that get_uncommitted_diff returns None for non-git directory."""
    result = get_uncommitted_diff(str(tmp_path))
    assert result is None
