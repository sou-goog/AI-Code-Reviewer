"""
Tests for main CLI module.
"""
import pytest
import os
import sys
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

# Import the app from main
from src.main import app

runner = CliRunner()


def test_version_command():
    """Test version command."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "1.0.0" in result.stdout
    assert "AI Code Reviewer" in result.stdout


def test_config_command():
    """Test config command."""
    result = runner.invoke(app, ["config", "test_key_123"])
    assert result.exit_code == 0
    assert "API Key Configuration" in result.stdout
    assert "test_key_123" in result.stdout


def test_doctor_command():
    """Test doctor command."""
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "System Health Check" in result.stdout
    assert "Python" in result.stdout


@patch('src.reviewer.run_review')
def test_review_command_staged(mock_review):
    """Test review command with staged diff."""
    mock_review.return_value = "## Review\nTest review"
    result = runner.invoke(app, ["review", "--diff-type", "staged"])
    assert result.exit_code == 0
    assert "Starting Code Review" in result.stdout


@patch('src.reviewer.run_review')
def test_review_command_markdown(mock_review):
    """Test review command with markdown output."""
    mock_review.return_value = "# Review\nTest"
    result = runner.invoke(app, ["review", "--format", "markdown"])
    assert result.exit_code == 0
    mock_review.assert_called_once()


@patch('src.reviewer.run_review')
def test_review_command_json(mock_review):
    """Test review command with JSON output."""
    mock_review.return_value = "Test review"
    result = runner.invoke(app, ["review", "--format", "json"])
    assert result.exit_code == 0
    # JSON output should be valid
    assert "diff_type" in result.stdout or "review" in result.stdout


@patch('src.database.ReviewDatabase')
def test_stats_command(mock_db_class):
    """Test stats command."""
    mock_db = MagicMock()
    mock_db.get_review_stats.return_value = {
        'total_reviews': 5,
        'total_issues': {'critical': 2, 'warning': 3, 'suggestion': 1},
        'avg_duration': 2.5
    }
    mock_db.get_recent_reviews.return_value = []
    mock_db_class.return_value = mock_db
    
    result = runner.invoke(app, ["stats"])
    assert result.exit_code == 0
    assert "Review Statistics" in result.stdout
    assert "5" in result.stdout  # Total reviews


def test_init_command_no_git(tmp_path, monkeypatch):
    """Test init command when not in git repo."""
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "Not a git repository" in result.stdout


def test_init_command_with_git(tmp_path, monkeypatch):
    """Test init command in git repo."""
    import subprocess
    # Create a git repo
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    monkeypatch.chdir(tmp_path)
    
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "Git repository detected" in result.stdout
