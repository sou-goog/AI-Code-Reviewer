import yaml
import os
import re
from typing import Dict, List, Optional

class ConfigManager:
    """Manages configuration from .codereview.yaml"""
    
    def __init__(self, config_path: str = ".codereview.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        if not os.path.exists(self.config_path):
            return self._default_config()
        
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config or self._default_config()
        except Exception as e:
            print(f"Warning: Could not load {self.config_path}: {e}")
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """Return default configuration."""
        return {
            'review': {
                'levels': 'all',
                'max_diff_size': 100,
                'ignore_patterns': [],
                'include_patterns': []
            },
            'model': {
                'name': 'gemini-2.5-flash',
                'temperature': 0.3
            },
            'custom_rules': []
        }
    
    def get_custom_rules(self) -> List[Dict]:
        """Get custom review rules."""
        return self.config.get('custom_rules', [])
    
    def get_model_name(self) -> str:
        """Get AI model name."""
        return self.config.get('model', {}).get('name', 'gemini-2.5-flash')
    
    def get_ignore_patterns(self) -> List[str]:
        """Get file patterns to ignore."""
        return self.config.get('review', {}).get('ignore_patterns', [])
    
    def should_review_file(self, filepath: str) -> bool:
        """Check if file should be reviewed based on patterns."""
        ignore_patterns = self.get_ignore_patterns()
        
        for pattern in ignore_patterns:
            # Simple glob pattern matching
            pattern_regex = pattern.replace('**/', '.*').replace('*', '[^/]*').replace('?', '.')
            if re.search(pattern_regex, filepath):
                return False
        
        return True


class CustomRulesEngine:
    """Applies custom review rules to code."""
    
    def __init__(self, rules: List[Dict]):
        self.rules = rules
    
    def apply_rules(self, diff: str) -> List[str]:
        """Apply custom rules and return findings."""
        findings = []
        
        for rule in self.rules:
            pattern = rule.get('pattern', '')
            message = rule.get('message', 'Custom rule matched')
            severity = rule.get('severity', 'info')
            
            if not pattern:
                continue
            
            # Find matches in diff
            matches = re.finditer(pattern, diff, re.IGNORECASE)
            match_count = sum(1 for _ in matches)
            
            if match_count > 0:
                emoji = self._severity_emoji(severity)
                finding = f"{emoji} **{severity.upper()}**: {message} ({match_count} occurrence(s))"
                findings.append(finding)
        
        return findings
    
    def _severity_emoji(self, severity: str) -> str:
        """Get emoji for severity level."""
        mapping = {
            'critical': '🔴',
            'warning': '🟡',
            'info': '🔵',
            'suggestion': '🟢'
        }
        return mapping.get(severity.lower(), 'ℹ️')
