# Example Review Output

This is an example of what the AI Code Reviewer generates.

## 🔍 Summary
This code change introduces a new authentication function with potential security vulnerabilities and code quality issues.

## 🔴 Critical Issues

### SQL Injection Vulnerability
**Location:** Line 15
```python
query = f"SELECT * FROM users WHERE username = '{user_input}'"
```
**Issue:** Using f-strings for SQL queries allows SQL injection attacks.

**Recommendation:** Use parameterized queries:
```python
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (user_input,))
```

### Hardcoded Credentials
**Location:** Line 23
```python
api_key = "sk-1234567890abcdef"
```
**Issue:** Hardcoded API keys in source code pose serious security risks.

**Recommendation:** Use environment variables:
```python
api_key = os.environ.get("API_KEY")
```

## 🟡 Warnings

### Missing Error Handling
**Location:** Lines 10-20
**Issue:** No try-except blocks around database operations.

**Recommendation:** Add proper error handling to catch and log exceptions.

### Unused Import
**Location:** Line 3
```python
import sys
```
**Issue:** Import is declared but never used.

**Recommendation:** Remove unused imports to keep code clean.

## 🟢 Suggestions

### Add Type Hints
**Recommendation:** Add type hints for better code documentation:
```python
def authenticate_user(username: str, password: str) -> bool:
```

### Add Docstrings
**Recommendation:** Document the function purpose and parameters:
```python
def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate a user with given credentials.
    
    Args:
        username: The user's username
        password: The user's password
        
    Returns:
        bool: True if authentication successful
    """
```

## ✅ Positive Notes

- Good variable naming conventions
- Consistent code formatting
- Logical function structure

---

**Review completed in 2.3 seconds**
