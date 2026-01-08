from .git_handler import get_staged_diff, get_uncommitted_diff, get_last_commit_diff
from .llm_client import analyze_code_diff
from .config import ConfigManager, CustomRulesEngine

def run_review(diff_type: str = "staged", output_format: str = "terminal"):
    """
    Orchestrates the code review process.
    
    Args:
        diff_type: Type of diff to review (staged, uncommitted, last-commit)
        output_format: Output format (terminal, markdown, json)
    """
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
    
    return report
