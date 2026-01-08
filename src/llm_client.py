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
    Analyze the following git diff and provide a code review.
    
    Focus on:
    1. Potential Bugs
    2. Security Vulnerabilities
    3. Code Style and Best Practices
    4. Performance Improvements

    Format your response in Markdown.

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
