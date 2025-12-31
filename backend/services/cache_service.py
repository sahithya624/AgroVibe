"""
Cache Service for SmartFarmingAI
Supports Redis with an in-memory fallback.
"""

import json
import logging
import functools
import hashlib
from typing import Any, Optional, Union, Callable
from datetime import timedelta

from backend.config import settings

logger = logging.getLogger(__name__)

# Use a global in-memory cache as fallback
_IN_MEMORY_CACHE = {}

class CacheService:
    def __init__(self):
        self.enabled = settings.ENABLE_CACHE
        self.redis_url = settings.REDIS_URL
        self.redis = None
        
        if self.enabled:
            try:
                import redis.asyncio as redis
                self.redis = redis.from_url(self.redis_url, decode_responses=True)
                logger.info(f"Connected to Redis at {self.redis_url}")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {e}. Falling back to in-memory cache.")
                self.redis = None

    async def get(self, key: str) -> Optional[Any]:
        if not self.enabled:
            return None
            
        if self.redis:
            try:
                value = await self.redis.get(key)
                return json.loads(value) if value else None
            except Exception as e:
                logger.error(f"Redis get error: {e}")
                return None
        else:
            return _IN_MEMORY_CACHE.get(key)

    async def set(self, key: str, value: Any, ttl: int = None):
        if not self.enabled:
            return
            
        ttl = ttl or settings.CACHE_TTL
        
        if self.redis:
            try:
                await self.redis.set(key, json.dumps(value), ex=ttl)
            except Exception as e:
                logger.error(f"Redis set error: {e}")
        else:
            _IN_MEMORY_CACHE[key] = value
            # In-memory TTL is not strictly enforced here for simplicity 
            # but could be added if needed.

    async def delete(self, key: str):
        if self.redis:
            await self.redis.delete(key)
        else:
            _IN_MEMORY_CACHE.pop(key, None)

_cache_service = None

def get_cache_service() -> CacheService:
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service

def cache_result(ttl: int = None, key_prefix: str = ""):
    """Decorator to cache function results."""
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cache = get_cache_service()
            if not cache.enabled:
                return await func(*args, **kwargs)

            # Create a unique key based on func name and args
            key_data = f"{func.__name__}:{args}:{kwargs}"
            key_hash = hashlib.md5(key_data.encode()).hexdigest()
            key = f"{key_prefix}:{key_hash}" if key_prefix else key_hash

            cached_val = await cache.get(key)
            if cached_val is not None:
                logger.info(f"Cache hit for {func.__name__}")
                return cached_val

            result = await func(*args, **kwargs)
            await cache.set(key, result, ttl)
            return result
        return wrapper
    return decorator
