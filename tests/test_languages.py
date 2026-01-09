"""
Tests for language detection and rules.
"""
import pytest
from src.languages import detect_language, get_language_rules, LANGUAGE_CONFIGS


def test_detect_language_python():
    """Test Python language detection."""
    assert detect_language("test.py") == "python"
    assert detect_language("src/main.py") == "python"
    assert detect_language("/path/to/file.py") == "python"


def test_detect_language_javascript():
    """Test JavaScript/TypeScript language detection."""
    assert detect_language("test.js") == "javascript"
    assert detect_language("component.jsx") == "javascript"
    assert detect_language("types.ts") == "javascript"
    assert detect_language("component.tsx") == "javascript"


def test_detect_language_java():
    """Test Java language detection."""
    assert detect_language("Main.java") == "java"
    assert detect_language("src/App.java") == "java"


def test_detect_language_go():
    """Test Go language detection."""
    assert detect_language("main.go") == "go"
    assert detect_language("handler.go") == "go"


def test_detect_language_rust():
    """Test Rust language detection."""
    assert detect_language("lib.rs") == "rust"
    assert detect_language("main.rs") == "rust"


def test_detect_language_unknown():
    """Test unknown language detection."""
    assert detect_language("file.txt") == "unknown"
    assert detect_language("file.xyz") == "unknown"
    assert detect_language("file") == "unknown"


def test_get_language_rules_python():
    """Test getting Python language rules."""
    rules = get_language_rules("python")
    assert len(rules) > 0
    assert any(rule["pattern"] == r"eval\(" for rule in rules)
    assert any(rule["pattern"] == r"exec\(" for rule in rules)


def test_get_language_rules_javascript():
    """Test getting JavaScript language rules."""
    rules = get_language_rules("javascript")
    assert len(rules) > 0
    assert any(rule["pattern"] == r"eval\(" for rule in rules)
    assert any("innerHTML" in rule["pattern"] for rule in rules)


def test_get_language_rules_unknown():
    """Test getting rules for unknown language."""
    rules = get_language_rules("unknown")
    assert rules == []


def test_language_configs_structure():
    """Test that all language configs have required fields."""
    for lang, config in LANGUAGE_CONFIGS.items():
        assert "file_extensions" in config
        assert "common_issues" in config
        assert isinstance(config["file_extensions"], list)
        assert isinstance(config["common_issues"], list)
        
        for issue in config["common_issues"]:
            assert "pattern" in issue
            assert "severity" in issue
            assert "message" in issue
