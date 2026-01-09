import re
import time
import json
from typing import Union, Dict, Any

from .config import ConfigManager, CustomRulesEngine
from .database import ReviewDatabase
from .git_handler import get_last_commit_diff, get_staged_diff, get_uncommitted_diff
from .llm_client import analyze_code_diff


def run_review(diff_type: str = "staged", output_format: str = "terminal", save_to_db: bool = True) -> Union[str, Dict[str, Any]]:
    """
    Orchestrates the code review process.
    
    Args:
        diff_type: Type of diff to review (staged, uncommitted, last-commit)
        output_format: Output format (terminal, markdown, json)
        save_to_db: Whether to save review to database

    Returns:
        Review report as string (markdown) or dict (json)
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
    
    # Determine the format to request from LLM
    # If output_format is json, request json. Otherwise markdown.
    llm_output_format = "json" if output_format == "json" else "markdown"

    # Run AI review
    report = analyze_code_diff(diff, config.get_model_name(), output_format=llm_output_format)
    
    # Apply custom rules
    # Note: Custom rules engine currently outputs strings. If in JSON mode, we should adapt this.
    custom_rules = config.get_custom_rules()
    custom_findings_list = []

    if custom_rules:
        rules_engine = CustomRulesEngine(custom_rules)
        custom_findings = rules_engine.apply_rules(diff)
        
        if custom_findings:
            if output_format == "json" and isinstance(report, dict):
                 # Convert text findings to objects for JSON output
                 for finding in custom_findings:
                    # Simple parsing of the existing finding string
                    # Expected format: "emoji **SEVERITY**: message (count)"
                    # This is brittle but sufficient for now
                    severity_match = re.search(r'\*\*(.*?)\*\*', finding)
                    severity = severity_match.group(1).lower() if severity_match else "info"

                    custom_findings_list.append({
                        "severity": severity,
                        "file": "N/A", # Custom rules based on regex might not know line/file easily without more logic
                        "line": "N/A",
                        "title": "Custom Rule Violation",
                        "description": finding,
                        "category": "custom_rule"
                    })

                 # Append to report issues
                 if "issues" not in report:
                     report["issues"] = []
                 report["issues"].extend(custom_findings_list)

            else:
                # Append text to markdown report
                report += "\n\n## 🎯 Custom Rules Findings\n\n"
                for finding in custom_findings:
                    report += f"- {finding}\n"
    
    # Save to database
    if save_to_db:
        duration = time.time() - start_time
        db = ReviewDatabase()
        
        # Count issues by severity
        if isinstance(report, dict):
            # JSON format
            issues = report.get("issues", [])
            critical_count = sum(1 for i in issues if i.get("severity") == "critical")
            warning_count = sum(1 for i in issues if i.get("severity") == "warning")
            suggestion_count = sum(1 for i in issues if i.get("severity") == "suggestion")

            # Serialize JSON report for storage
            review_text = json.dumps(report)
        else:
            # Markdown format
            critical_count = len(re.findall(r'🔴|Critical', report, re.IGNORECASE))
            warning_count = len(re.findall(r'🟡|Warning', report, re.IGNORECASE))
            suggestion_count = len(re.findall(r'🟢|Suggestion', report, re.IGNORECASE))
            review_text = report
        
        review_data = {
            'diff_type': diff_type,
            'file_count': len(re.findall(r'diff --git', diff)),
            'critical_count': critical_count,
            'warning_count': warning_count,
            'suggestion_count': suggestion_count,
            'review_text': review_text,
            'duration_seconds': duration
        }
        
        db.save_review(review_data)
    
    # If output_format is json but report is dict, we return the dict.
    # The CLI (src/main.py) handles converting the dict to a JSON string if needed.
    # However, if output_format is terminal/markdown, we expect a string.

    return report
