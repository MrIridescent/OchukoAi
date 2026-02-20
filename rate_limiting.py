"""
Phase 3: Advanced Rate Limiting System
Sliding window, per-endpoint, adaptive limits with token bucket algorithm
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from collections import defaultdict
import asyncio

from logging_system import StructuredLogger

logger = StructuredLogger(__name__)


class TokenBucket:
    """Token bucket for rate limiting with refill"""
    
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.tokens = capacity
        self.last_refill = datetime.utcnow()
    
    def refill(self):
        """Refill bucket based on time elapsed"""
        now = datetime.utcnow()
        elapsed = (now - self.last_refill).total_seconds()
        new_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill = now
    
    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens from bucket"""
        self.refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


class SlidingWindowLimiter:
    """Sliding window rate limiter with per-second resolution"""
    
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed"""
        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=self.window_seconds)
        
        if identifier not in self.requests:
            self.requests[identifier] = []
        
        self.requests[identifier] = [
            ts for ts in self.requests[identifier] if ts > cutoff
        ]
        
        if len(self.requests[identifier]) < self.limit:
            self.requests[identifier].append(now)
            return True
        
        return False
    
    def get_retry_after(self, identifier: str) -> int:
        """Get seconds until next request is allowed"""
        if identifier not in self.requests or not self.requests[identifier]:
            return 0
        
        oldest = self.requests[identifier][0]
        retry_after = (oldest + timedelta(seconds=self.window_seconds) - datetime.utcnow()).total_seconds()
        return max(0, int(retry_after) + 1)


class AdaptiveRateLimiter:
    """Adaptive rate limiting based on system load"""
    
    def __init__(self):
        self.default_limiter = SlidingWindowLimiter(limit=100, window_seconds=60)
        self.strict_limiter = SlidingWindowLimiter(limit=10, window_seconds=60)
        self.generous_limiter = SlidingWindowLimiter(limit=1000, window_seconds=60)
        
        self.system_load = 0.0  # 0.0 to 1.0
        self.endpoint_rates: Dict[str, int] = defaultdict(lambda: 0)
        self.failing_endpoints: set = set()
    
    def record_failure(self, endpoint: str):
        """Record endpoint failure"""
        self.failing_endpoints.add(endpoint)
        logger.warning("Endpoint marked as failing", endpoint=endpoint)
    
    def record_success(self, endpoint: str):
        """Record endpoint success"""
        self.failing_endpoints.discard(endpoint)
    
    def update_system_load(self, load: float):
        """Update current system load (0.0 to 1.0)"""
        self.system_load = max(0.0, min(1.0, load))
    
    def get_limiter(self, endpoint: str) -> SlidingWindowLimiter:
        """Get appropriate limiter based on load and endpoint status"""
        if endpoint in self.failing_endpoints:
            logger.debug("Using strict limiter for failing endpoint", endpoint=endpoint)
            return self.strict_limiter
        
        if self.system_load > 0.8:
            logger.debug("Using strict limiter due to high load", load=self.system_load)
            return self.strict_limiter
        
        if self.system_load < 0.3:
            logger.debug("Using generous limiter due to low load", load=self.system_load)
            return self.generous_limiter
        
        return self.default_limiter
    
    async def is_allowed(self, identifier: str, endpoint: str) -> Tuple[bool, Optional[int]]:
        """Check if request is allowed, return (allowed, retry_after_seconds)"""
        limiter = self.get_limiter(endpoint)
        allowed = limiter.is_allowed(f"{identifier}:{endpoint}")
        
        if not allowed:
            retry_after = limiter.get_retry_after(f"{identifier}:{endpoint}")
            logger.warning(
                "Rate limit exceeded",
                identifier=identifier,
                endpoint=endpoint,
                retry_after=retry_after
            )
            return False, retry_after
        
        return True, None


class PerEndpointLimiter:
    """Per-endpoint rate limiting with customizable limits"""
    
    def __init__(self):
        self.limits: Dict[str, SlidingWindowLimiter] = {}
        self.default_limit = 100
        self.default_window = 60
    
    def set_limit(self, endpoint: str, limit: int, window_seconds: int):
        """Set custom limit for endpoint"""
        self.limits[endpoint] = SlidingWindowLimiter(limit, window_seconds)
        logger.info("Endpoint limit set", endpoint=endpoint, limit=limit, window=window_seconds)
    
    def get_limiter(self, endpoint: str) -> SlidingWindowLimiter:
        """Get limiter for endpoint, create if not exists"""
        if endpoint not in self.limits:
            self.limits[endpoint] = SlidingWindowLimiter(
                self.default_limit, 
                self.default_window
            )
        return self.limits[endpoint]
    
    async def is_allowed(self, identifier: str, endpoint: str) -> Tuple[bool, Optional[int]]:
        """Check if request is allowed"""
        limiter = self.get_limiter(endpoint)
        key = f"{identifier}:{endpoint}"
        allowed = limiter.is_allowed(key)
        
        if not allowed:
            retry_after = limiter.get_retry_after(key)
            return False, retry_after
        
        return True, None


class RateLimitingMiddleware:
    """FastAPI middleware for rate limiting"""
    
    def __init__(self, adaptive: bool = True):
        self.adaptive = AdaptiveRateLimiter() if adaptive else None
        self.per_endpoint = PerEndpointLimiter()
    
    async def check_limit(
        self,
        client_id: str,
        endpoint: str,
        user_id: Optional[str] = None
    ) -> Tuple[bool, Optional[int]]:
        """Check rate limit for request"""
        identifier = user_id or client_id
        
        if self.adaptive:
            return await self.adaptive.is_allowed(identifier, endpoint)
        
        return await self.per_endpoint.is_allowed(identifier, endpoint)
    
    def set_endpoint_limit(self, endpoint: str, limit: int, window_seconds: int = 60):
        """Configure limit for specific endpoint"""
        self.per_endpoint.set_limit(endpoint, limit, window_seconds)


global_rate_limiter = RateLimitingMiddleware(adaptive=True)
