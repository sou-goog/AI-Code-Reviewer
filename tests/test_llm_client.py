import pytest
import os
from unittest.mock import patch, MagicMock
from src.llm_client import analyze_code_diff

@patch('src.llm_client._call_gemini_api')
def test_analyze_code_diff_success(mock_api_call):
    """Test successful code diff analysis."""
    os.environ['GEMINI_API_KEY'] = 'test_key'
    
    mock_api_call.return_value = "## Review\nNo issues found"
    
    result = analyze_code_diff("diff --git a/test.py", "gemini-2.5-flash", use_cache=False)
    
    assert "Review" in result
    assert "No issues found" in result
    mock_api_call.assert_called_once()

def test_analyze_code_diff_no_api_key():
    """Test analysis without API key."""
    original_key = os.environ.pop('GEMINI_API_KEY', None)
    try:
        with pytest.raises(Exception) as exc_info:
            analyze_code_diff("diff --git a/test.py")
        assert "GEMINI_API_KEY" in str(exc_info.value)
    finally:
        if original_key:
            os.environ['GEMINI_API_KEY'] = original_key

@patch('src.llm_client._call_gemini_api')
def test_analyze_code_diff_api_error(mock_api_call):
    """Test handling of API errors."""
    os.environ['GEMINI_API_KEY'] = 'test_key'
    
    from src.utils.retry import ReviewError
    mock_api_call.side_effect = ReviewError("API Error: Failed to analyze code")
    
    with pytest.raises(ReviewError) as exc_info:
        analyze_code_diff("diff --git a/test.py", use_cache=False)
    
    assert "API Error" in str(exc_info.value) or "Failed to analyze" in str(exc_info.value)
