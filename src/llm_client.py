import os
import google.generativeai as genai
from typing import Optional

def analyze_code_diff(diff: str) -> Optional[str]:
    """
    Sends the git diff to Google Gemini for analysis.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY environment variable not set."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    You are an expert Senior Software Engineer and Code Reviewer.
    Analyze the following git diff and provide a comprehensive code review.
    
    FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:
    
    ## 🔍 Summary
    [Brief overview of changes]
    
    ## 🔴 Critical Issues
    [List critical bugs, security vulnerabilities - things that MUST be fixed]
    
    ## 🟡 Warnings
    [List potential problems, code smells, things that SHOULD be fixed]
    
    ## 🟢 Suggestions
    [List style improvements, best practices, nice-to-haves]
    
    ## ✅ Positive Notes
    [Highlight good practices, improvements]
    
    Focus on:
    1. **Security Vulnerabilities** - SQL injection, XSS, secrets in code, etc.
    2. **Bugs** - Logic errors, null pointer exceptions, race conditions
    3. **Performance** - Inefficient algorithms, memory leaks
    4. **Code Quality** - Naming, structure, maintainability
    5. **Best Practices** - Language-specific conventions
    
    Be specific. Reference line numbers if possible. Provide concrete suggestions.

    GIT DIFF:
    ```diff
    {diff}
    ```
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini API: {e}"
