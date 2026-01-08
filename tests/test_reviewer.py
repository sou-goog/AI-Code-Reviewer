import pytest
from src.reviewer import run_review
from unittest.mock import patch, MagicMock

def test_run_review_with_no_changes():
    """Test review when no changes are found."""
    with patch('src.reviewer.get_staged_diff', return_value=None):
        result = run_review(diff_type="staged")
        assert "No staged changes found" in result

def test_run_review_with_invalid_diff_type():
    """Test review with invalid diff type."""
    result = run_review(diff_type="invalid_type")
    assert "Error: Invalid diff type" in result

@patch('src.reviewer.analyze_code_diff')
@patch('src.reviewer.get_staged_diff')
def test_run_review_basic_flow(mock_get_diff, mock_analyze):
    """Test basic review flow."""
    mock_get_diff.return_value = "diff --git a/test.py"
    mock_analyze.return_value = "## Review\nNo issues found"
    
    result = run_review(diff_type="staged")
    
    assert "Review" in result
    mock_get_diff.assert_called_once()
    mock_analyze.assert_called_once()

@patch('src.reviewer.ConfigManager')
@patch('src.reviewer.analyze_code_diff')
@patch('src.reviewer.get_staged_diff')
def test_run_review_with_custom_rules(mock_get_diff, mock_analyze, mock_config):
    """Test review with custom rules."""
    mock_get_diff.return_value = "diff --git a/test.py\n+print('test')"
    mock_analyze.return_value = "## Review\nNo issues"
    
    mock_config_instance = MagicMock()
    mock_config_instance.get_custom_rules.return_value = [
        {
            'pattern': 'print\\(',
            'message': 'Debug statement found',
            'severity': 'warning'
        }
    ]
    mock_config_instance.get_model_name.return_value = 'gemini-2.5-flash'
    mock_config.return_value = mock_config_instance
    
    result = run_review(diff_type="staged")
    
    assert "Custom Rules Findings" in result
    assert "Debug statement found" in result
