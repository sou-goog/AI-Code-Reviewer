import pytest
import os
from unittest.mock import patch, MagicMock
from src.llm_client import analyze_code_diff

@patch('src.llm_client.genai.GenerativeModel')
@patch('src.llm_client.genai.configure')
def test_analyze_code_diff_success(mock_configure, mock_model_class):
    """Test successful code diff analysis."""
    os.environ['GEMINI_API_KEY'] = 'test_key'
    
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "## Review\nNo issues found"
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model
    
    result = analyze_code_diff("diff --git a/test.py", "gemini-2.5-flash")
    
    assert "Review" in result
    assert "No issues found" in result
    mock_configure.assert_called_once_with(api_key='test_key')

def test_analyze_code_diff_no_api_key():
    """Test analysis without API key."""
    if 'GEMINI_API_KEY' in os.environ:
        del os.environ['GEMINI_API_KEY']
    
    result = analyze_code_diff("diff --git a/test.py")
    
    assert "GEMINI_API_KEY environment variable not set" in result

@patch('src.llm_client.genai.GenerativeModel')
@patch('src.llm_client.genai.configure')
def test_analyze_code_diff_api_error(mock_configure, mock_model_class):
    """Test handling of API errors."""
    os.environ['GEMINI_API_KEY'] = 'test_key'
    
    mock_model = MagicMock()
    mock_model.generate_content.side_effect = Exception("API Error")
    mock_model_class.return_value = mock_model
    
    result = analyze_code_diff("diff --git a/test.py")
    
    assert "Error communicating with Gemini API" in result
