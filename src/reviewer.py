import re
import time

from .config import ConfigManager, CustomRulesEngine
from .database import ReviewDatabase
from .git_handler import get_last_commit_diff, get_staged_diff, get_uncommitted_diff
from .llm_client import analyze_code_diff


def run_review(diff_type: str = "staged", output_format: str = "terminal", save_to_db: bool = True):
    """
    Orchestrates the code review process.
    
    Args:
        diff_type: Type of diff to review (staged, uncommitted, last-commit)
        output_format: Output format (terminal, markdown, json)
        save_to_db: Whether to save review to database
    """
    start_time = time.time()
    
    # Load configuration
    config = ConfigManager()
    
    # Get the appropriate diff
    if diff_type == "staged":
        diff = get_staged_diff()
    elif diff_type == "uncommitted":
        diff = get_uncommitted_diff()
    elif diff_type == "last-commit":
        diff = get_last_commit_diff()
    else:
        return f"Error: Invalid diff type '{diff_type}'"
    
    if not diff:
        return f"No {diff_type} changes found to review."
    
    # Run AI review
    report = analyze_code_diff(diff, config.get_model_name())
    
    # Apply custom rules
    custom_rules = config.get_custom_rules()
    if custom_rules:
        rules_engine = CustomRulesEngine(custom_rules)
        custom_findings = rules_engine.apply_rules(diff)
        
        if custom_findings:
            report += "\n\n## 🎯 Custom Rules Findings\n\n"
            for finding in custom_findings:
                report += f"- {finding}\n"
    
    # Save to database
    if save_to_db:
        duration = time.time() - start_time
        db = ReviewDatabase()
        
        # Count issues by severity
        critical_count = len(re.findall(r'🔴|Critical', report, re.IGNORECASE))
        warning_count = len(re.findall(r'🟡|Warning', report, re.IGNORECASE))
        suggestion_count = len(re.findall(r'🟢|Suggestion', report, re.IGNORECASE))
        
        review_data = {
            'diff_type': diff_type,
            'file_count': len(re.findall(r'diff --git', diff)),
            'critical_count': critical_count,
            'warning_count': warning_count,
            'suggestion_count': suggestion_count,
            'review_text': report,
            'duration_seconds': duration
        }
        
        db.save_review(review_data)
    
    return report
