"""
LLM client for interacting with Google Gemini API.
Includes retry logic, caching, and comprehensive error handling.
"""
import logging
import os
from typing import Optional

import google.generativeai as genai

from src.utils.cache import ReviewCache
from src.utils.retry import RateLimitError, ReviewError, TimeoutError, retry_with_backoff

logger = logging.getLogger(__name__)


def analyze_code_diff(
    diff: str,
    model_name: str = "gemini-2.5-flash",
    use_cache: bool = True,
    timeout: Optional[int] = None
) -> str:
    """
    Analyze a code diff using Google Gemini AI.
    
    Args:
        diff: Git diff string to analyze
        model_name: Gemini model to use
        use_cache: Whether to use caching (default: True)
        timeout: Optional timeout in seconds
        
    Returns:
        AI-generated review as markdown string
        
    Raises:
        ReviewError: If API key not set or review fails
        RateLimitError: If API rate limit exceeded
        TimeoutError: If request times out
    """
    # Check for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ReviewError(
            "GEMINI_API_KEY environment variable not set. "
            "Get one at: https://aistudio.google.com/app/apikey"
        )
    
    # Check cache if enabled
    if use_cache:
        cache = ReviewCache()
        cache_key = cache.get_cache_key(diff, model_name)
        cached_review = cache.get(cache_key)
        
        if cached_review:
            logger.info("Using cached review")
            return cached_review.get('review', '')
    
    # Call API with retry logic
    try:
        review = _call_gemini_api(diff, model_name, api_key, timeout)
        
        # Cache the result
        if use_cache:
            cache.set(cache_key, {'review': review, 'model': model_name})
        
        return review
        
    except Exception as e:
        logger.error(f"Review failed: {e}")
        raise ReviewError(f"Failed to analyze code: {e}") from e


@retry_with_backoff(
    max_attempts=3,
    base_delay=2.0,
    exceptions=(Exception,)
)
def _call_gemini_api(
    diff: str,
    model_name: str,
    api_key: str,
    timeout: Optional[int]
) -> str:
    """
    Internal function to call Gemini API with retry logic.
    
    Args:
        diff: Code diff
        model_name: Model to use
        api_key: API key
        timeout: Timeout in seconds
        
    Returns:
        Review text
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""
You are an expert code reviewer. Analyze this git diff and provide a comprehensive code review.

Categorize your findings into sections:

## 🔴 Critical Issues
- Security vulnerabilities (SQL injection, XSS, hardcoded secrets)
- Logic errors that will cause bugs
- Breaking changes

## 🟡 Warnings
- Code smells
- Potential performance issues
- Missing error handling

## 🟢 Suggestions
- Best practice improvements
- Refactoring opportunities
- Performance optimizations

## ✅ Positive Notes
- Good practices
- Well-written code
- Clever solutions

GIT DIFF:
```diff
{diff}
```
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        error_msg = str(e).lower()
        
        # Detect rate limiting
        if "rate" in error_msg or "quota" in error_msg or "429" in error_msg:
            raise RateLimitError(f"API rate limit exceeded: {e}") from e
        
        # Detect timeout
        if "timeout" in error_msg or "deadline" in error_msg:
            raise TimeoutError(f"API request timed out: {e}") from e
        
        # Generic error
        raise ReviewError(f"API error: {e}") from e
