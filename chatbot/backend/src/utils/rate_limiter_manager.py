"""
rate_limiter_manager.py

This module provides functions to create thread-safe in-memory rate limiters for LLM API usage.
"""
from langchain_core.rate_limiters import InMemoryRateLimiter

def create_rate_limiter_from_config(config: dict):
    """
    Create a new InMemoryRateLimiter from a config dict with keys:
    - requests_per_minute
    - check_every_n_seconds
    - max_bucket_size
    """
    requests_per_second = config["requests_per_minute"] / 60.0
    return InMemoryRateLimiter(
        requests_per_second=requests_per_second,
        check_every_n_seconds=config["check_every_n_seconds"],
        max_bucket_size=config["max_bucket_size"],
    )
