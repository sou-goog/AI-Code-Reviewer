"""
Tests for retry logic.
"""
import pytest
from src.utils.retry import retry_with_backoff, RateLimitError, TimeoutError, ReviewError


def test_retry_success_first_attempt():
    """Test function succeeds on first attempt."""
    call_count = 0
    
    @retry_with_backoff(max_attempts=3)
    def succeeds_immediately():
        nonlocal call_count
        call_count += 1
        return "success"
    
    result = succeeds_immediately()
    
    assert result == "success"
    assert call_count == 1


def test_retry_success_after_failures():
    """Test function succeeds after some failures."""
    call_count = 0
    
    @retry_with_backoff(max_attempts=3, base_delay=0.1)
    def succeeds_on_third_try():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("Temporary error")
        return "success"
    
    result = succeeds_on_third_try()
    
    assert result == "success"
    assert call_count == 3


def test_retry_max_attempts_exceeded():
    """Test function fails after max attempts."""
    call_count = 0
    
    @retry_with_backoff(max_attempts=3, base_delay=0.1)
    def always_fails():
        nonlocal call_count
        call_count += 1
        raise ValueError("Permanent error")
    
    with pytest.raises(ValueError, match="Permanent error"):
        always_fails()
    
    assert call_count == 3


def test_retry_specific_exceptions():
    """Test retry only catches specified exceptions."""
    call_count = 0
    
    @retry_with_backoff(max_attempts=3, exceptions=(ValueError,))
    def raises_type_error():
        nonlocal call_count
        call_count += 1
        raise TypeError("Should not retry")
    
    with pytest.raises(TypeError, match="Should not retry"):
        raises_type_error()
    
    # Should fail on first attempt (no retry for TypeError)
    assert call_count == 1
