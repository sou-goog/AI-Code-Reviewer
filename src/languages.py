# Multi-Language Support Configuration

# Language-specific patterns and best practices
LANGUAGE_CONFIGS = {
    "python": {
        "file_extensions": [".py"],
        "common_issues": [
            {"pattern": r"eval\(", "severity": "critical", "message": "Avoid eval() - security risk"},
            {"pattern": r"exec\(", "severity": "critical", "message": "Avoid exec() - security risk"},
            {"pattern": r"pickle\.loads?\(", "severity": "warning", "message": "Pickle can execute arbitrary code"},
            {"pattern": r"^\s*print\(", "severity": "info", "message": "Debug print statement"},
        ]
    },
    "javascript": {
        "file_extensions": [".js", ".jsx", ".ts", ".tsx"],
        "common_issues": [
            {"pattern": r"eval\(", "severity": "critical", "message": "Avoid eval() - security risk"},
            {"pattern": r"innerHTML\s*=", "severity": "critical", "message": "XSS risk - use textContent or sanitize"},
            {"pattern": r"console\.log\(", "severity": "info", "message": "Remove debug console.log"},
            {"pattern": r"==\s", "severity": "warning", "message": "Use === for strict equality"},
        ]
    },
    "java": {
        "file_extensions": [".java"],
        "common_issues": [
            {"pattern": r"Runtime\.getRuntime\(\)\.exec", "severity": "critical", "message": "Command injection risk"},
            {"pattern": r"System\.out\.print", "severity": "info", "message": "Use logging instead of System.out"},
            {"pattern": r"catch\s*\(\s*Exception\s+\w+\s*\)\s*\{\s*\}", "severity": "warning", "message": "Empty catch block"},
        ]
    },
    "go": {
        "file_extensions": [".go"],
        "common_issues": [
            {"pattern": r"panic\(", "severity": "warning", "message": "Consider returning error instead of panic"},
            {"pattern": r"//\s*TODO", "severity": "info", "message": "TODO comment found"},
            {"pattern": r"fmt\.Print", "severity": "info", "message": "Consider using structured logging"},
        ]
    },
    "rust": {
        "file_extensions": [".rs"],
        "common_issues": [
            {"pattern": r"unwrap\(\)", "severity": "warning", "message": "Avoid unwrap() - handle errors explicitly"},
            {"pattern": r"expect\(", "severity": "info", "message": "Consider proper error handling"},
            {"pattern": r"unsafe\s*\{", "severity": "warning", "message": "Unsafe block requires careful review"},
        ]
    }
}

def detect_language(file_path: str) -> str:
    """Detect programming language from file extension."""
    for lang, config in LANGUAGE_CONFIGS.items():
        for ext in config["file_extensions"]:
            if file_path.endswith(ext):
                return lang
    return "unknown"

def get_language_rules(language: str):
    """Get language-specific review rules."""
    return LANGUAGE_CONFIGS.get(language, {}).get("common_issues", [])
