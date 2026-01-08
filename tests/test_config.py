import pytest
import os
import tempfile
from src.config import ConfigManager, CustomRulesEngine

def test_config_manager_default():
    """Test ConfigManager with no config file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, 'nonexistent.yaml')
        config = ConfigManager(config_path)
        
        assert config.get_model_name() == 'gemini-2.5-flash'
        assert config.get_custom_rules() == []
        assert config.get_ignore_patterns() == []

def test_custom_rules_engine():
    """Test custom rules engine."""
    rules = [
        {
            'pattern': 'TODO',
            'message': 'TODO found',
            'severity': 'warning'
        },
        {
            'pattern': 'console\\.log',
            'message': 'Debug statement',
            'severity': 'info'
        }
    ]
    
    engine = CustomRulesEngine(rules)
    diff = """
    + // TODO: Fix this later
    + console.log('debug');
    """
    
    findings = engine.apply_rules(diff)
    
    assert len(findings) == 2
    assert 'TODO found' in findings[0]
    assert 'Debug statement' in findings[1]

def test_custom_rules_no_matches():
    """Test custom rules with no matches."""
    rules = [
        {
            'pattern': 'FIXME',
            'message': 'FIXME found',
            'severity': 'warning'
        }
    ]
    
    engine = CustomRulesEngine(rules)
    diff = "+ print('hello world')"
    
    findings = engine.apply_rules(diff)
    
    assert len(findings) == 0
