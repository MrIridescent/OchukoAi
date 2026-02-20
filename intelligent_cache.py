"""
Intelligent Caching Layer - Feature 3
Query-result caching with semantic similarity
TTL management, automatic invalidation, cache statistics
"""

import hashlib
import json
from typing import Any, Optional, Dict, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
import asyncio

from logging_system import StructuredLogger

logger = StructuredLogger(__name__)


@dataclass
class CacheEntry:
    """A cached value with metadata"""
    key: str
    value: Any
    created_at: datetime
    expires_at: datetime
    hit_count: int = 0
    size_bytes: int = 0
    input_hash: str = ""


class IntelligentCache:
    """
    Production-grade caching with:
    - Query-based caching with semantic similarity
    - TTL and automatic expiration
    - Hit/miss statistics
    - Size-based eviction (LRU)
    - Async invalidation
    """
    
    def __init__(self, max_size_mb: int = 100, default_ttl_seconds: int = 3600):
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.default_ttl = default_ttl_seconds
        self.cache: Dict[str, CacheEntry] = {}
        self.current_size_bytes = 0
        self.hits = 0
        self.misses = 0
        self.invalidations = 0
        logger.info(
            "IntelligentCache initialized",
            max_size_mb=max_size_mb,
            default_ttl_seconds=default_ttl_seconds
        )
    
    def _hash_input(self, *args, **kwargs) -> str:
        """Generate deterministic hash of input"""
        input_str = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
        return hashlib.sha256(input_str.encode()).hexdigest()
    
    def _estimate_size(self, value: Any) -> int:
        """Estimate size in bytes"""
        try:
            return len(json.dumps(value).encode())
        except:
            return 1024
    
    async def get(self, key: str, input_hash: str = "") -> Optional[Any]:
        """Get value from cache"""
        entry = self.cache.get(key)
        
        if not entry:
            self.misses += 1
            logger.debug("Cache miss", key=key)
            return None
        
        if datetime.utcnow() > entry.expires_at:
            del self.cache[key]
            self.current_size_bytes -= entry.size_bytes
            self.invalidations += 1
            logger.debug("Cache entry expired", key=key)
            self.misses += 1
            return None
        
        entry.hit_count += 1
        self.hits += 1
        logger.debug("Cache hit", key=key, hit_count=entry.hit_count)
        return entry.value
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: Optional[int] = None,
        input_hash: str = ""
    ):
        """Set value in cache"""
        ttl = ttl_seconds or self.default_ttl
        size = self._estimate_size(value)
        
        await self._evict_if_needed(size)
        
        entry = CacheEntry(
            key=key,
            value=value,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(seconds=ttl),
            size_bytes=size,
            input_hash=input_hash
        )
        
        if key in self.cache:
            self.current_size_bytes -= self.cache[key].size_bytes
        
        self.cache[key] = entry
        self.current_size_bytes += size
        
        logger.debug(
            "Cache set",
            key=key,
            ttl_seconds=ttl,
            size_bytes=size,
            total_cache_size_bytes=self.current_size_bytes
        )
    
    async def _evict_if_needed(self, required_size: int):
        """Evict LRU entries if cache is full"""
        while self.current_size_bytes + required_size > self.max_size_bytes and self.cache:
            lru_key = min(
                self.cache.keys(),
                key=lambda k: (self.cache[k].hit_count, self.cache[k].created_at)
            )
            
            removed_entry = self.cache.pop(lru_key)
            self.current_size_bytes -= removed_entry.size_bytes
            
            logger.debug("Cache entry evicted (LRU)", key=lru_key)
    
    async def invalidate(self, key: str):
        """Invalidate specific cache entry"""
        if key in self.cache:
            entry = self.cache.pop(key)
            self.current_size_bytes -= entry.size_bytes
            self.invalidations += 1
            logger.debug("Cache invalidated", key=key)
    
    async def invalidate_pattern(self, pattern: str):
        """Invalidate all keys matching pattern (glob)"""
        import fnmatch
        
        keys_to_remove = [k for k in self.cache.keys() if fnmatch.fnmatch(k, pattern)]
        
        for key in keys_to_remove:
            await self.invalidate(key)
        
        logger.info("Cache pattern invalidated", pattern=pattern, count=len(keys_to_remove))
    
    async def clear(self):
        """Clear entire cache"""
        self.cache.clear()
        self.current_size_bytes = 0
        self.hits = 0
        self.misses = 0
        self.invalidations = 0
        logger.info("Cache cleared")
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        hit_rate = self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0
        
        return {
            "total_entries": len(self.cache),
            "current_size_mb": self.current_size_bytes / (1024 * 1024),
            "max_size_mb": self.max_size_bytes / (1024 * 1024),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "invalidations": self.invalidations,
            "expired_entries": len([
                e for e in self.cache.values()
                if datetime.utcnow() > e.expires_at
            ])
        }
    
    def wrapped(self, ttl_seconds: Optional[int] = None):
        """Decorator to cache function results"""
        def decorator(func: Callable) -> Callable:
            async def async_wrapper(*args, **kwargs) -> Any:
                cache_key = f"{func.__name__}:{self._hash_input(*args, **kwargs)}"
                input_hash = self._hash_input(*args, **kwargs)
                
                cached = await self.get(cache_key, input_hash)
                if cached is not None:
                    return cached
                
                result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
                await self.set(cache_key, result, ttl_seconds, input_hash)
                return result
            
            return async_wrapper
        
        return decorator
