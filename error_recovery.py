"""
Intelligent Error Recovery System - Feature 6
Graceful fallback when APIs fail
Cache-based recovery, quality metrics per response
"""

import asyncio
from typing import Any, Optional, Callable, Dict
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from logging_system import StructuredLogger

logger = StructuredLogger(__name__)


class RecoveryStrategy(Enum):
    FALLBACK_CACHE = "fallback_cache"
    FALLBACK_MODEL = "fallback_model"
    GRACEFUL_DEGRADATION = "graceful_degradation"
    RETRY = "retry"
    CIRCUIT_BREAK = "circuit_break"


@dataclass
class RecoveryResult:
    """Result with quality metrics"""
    data: Any
    success: bool
    strategy: RecoveryStrategy
    quality_score: float
    latency_ms: float
    error: Optional[str] = None
    recovered: bool = False


class ErrorRecoverySystem:
    """
    Handles failures with multiple recovery strategies:
    - Cache-based fallback (serve stale data)
    - Alternative model fallback (GPT-4 → Claude)
    - Graceful degradation (return partial result)
    - Automatic retries with backoff
    - Circuit breaking for cascading failures
    """
    
    def __init__(self, cache_system=None):
        self.cache = cache_system
        self.fallback_models: Dict[str, Callable] = {}
        self.circuit_breakers: Dict[str, 'CircuitBreakerState'] = {}
        self.recovery_stats = {
            "total_recoveries": 0,
            "cache_hits": 0,
            "fallback_successes": 0,
            "degraded_responses": 0,
            "failed_recoveries": 0
        }
        logger.info("ErrorRecoverySystem initialized")
    
    async def execute_with_recovery(
        self,
        primary_func: Callable,
        primary_name: str,
        *args,
        fallback_funcs: Optional[Dict[str, Callable]] = None,
        cache_key: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 2,
        **kwargs
    ) -> RecoveryResult:
        """
        Execute with multiple fallback strategies
        1. Try primary function
        2. Retry with backoff
        3. Check cache
        4. Try fallback functions
        5. Graceful degradation
        """
        start_time = datetime.utcnow()
        
        for attempt in range(max_retries + 1):
            try:
                result = await asyncio.wait_for(
                    primary_func(*args, **kwargs) if asyncio.iscoroutinefunction(primary_func) 
                    else asyncio.to_thread(primary_func, *args, **kwargs),
                    timeout=timeout
                )
                
                latency = (datetime.utcnow() - start_time).total_seconds() * 1000
                
                logger.info(
                    f"Primary execution succeeded: {primary_name}",
                    latency_ms=latency,
                    attempt=attempt
                )
                
                return RecoveryResult(
                    data=result,
                    success=True,
                    strategy=RecoveryStrategy.RETRY if attempt > 0 else RecoveryStrategy.RETRY,
                    quality_score=1.0,
                    latency_ms=latency
                )
            
            except Exception as e:
                logger.warning(
                    f"Primary execution failed: {primary_name}",
                    error=str(e),
                    attempt=attempt
                )
                
                if attempt < max_retries:
                    backoff = min(2 ** attempt, 10)
                    await asyncio.sleep(backoff)
                    continue
        
        if cache_key and self.cache:
            cached = await self.cache.get(cache_key)
            if cached:
                self.recovery_stats["cache_hits"] += 1
                latency = (datetime.utcnow() - start_time).total_seconds() * 1000
                
                logger.info(
                    f"Served from cache: {cache_key}",
                    latency_ms=latency,
                    quality_score=0.8
                )
                
                return RecoveryResult(
                    data=cached,
                    success=True,
                    strategy=RecoveryStrategy.FALLBACK_CACHE,
                    quality_score=0.8,
                    latency_ms=latency,
                    recovered=True
                )
        
        if fallback_funcs:
            for fallback_name, fallback_func in fallback_funcs.items():
                try:
                    result = await asyncio.wait_for(
                        fallback_func(*args, **kwargs) if asyncio.iscoroutinefunction(fallback_func)
                        else asyncio.to_thread(fallback_func, *args, **kwargs),
                        timeout=timeout
                    )
                    
                    self.recovery_stats["fallback_successes"] += 1
                    latency = (datetime.utcnow() - start_time).total_seconds() * 1000
                    
                    logger.info(
                        f"Fallback succeeded: {fallback_name}",
                        latency_ms=latency,
                        quality_score=0.7
                    )
                    
                    return RecoveryResult(
                        data=result,
                        success=True,
                        strategy=RecoveryStrategy.FALLBACK_MODEL,
                        quality_score=0.7,
                        latency_ms=latency,
                        recovered=True
                    )
                
                except Exception as e:
                    logger.warning(f"Fallback failed: {fallback_name}", error=str(e))
                    continue
        
        self.recovery_stats["degraded_responses"] += 1
        latency = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        degraded_response = self._generate_degraded_response(args, kwargs)
        
        logger.warning(
            "Returning degraded response",
            latency_ms=latency,
            quality_score=0.3
        )
        
        return RecoveryResult(
            data=degraded_response,
            success=False,
            strategy=RecoveryStrategy.GRACEFUL_DEGRADATION,
            quality_score=0.3,
            latency_ms=latency,
            error="All recovery strategies exhausted",
            recovered=True
        )
    
    def _generate_degraded_response(self, args: tuple, kwargs: dict) -> Dict[str, Any]:
        """Generate minimal valid response for graceful degradation"""
        return {
            "status": "degraded",
            "message": "Service temporarily unavailable. Returning cached or placeholder response.",
            "data": None,
            "quality_score": 0.3,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def get_recovery_stats(self) -> Dict[str, Any]:
        """Get recovery statistics"""
        total = self.recovery_stats["total_recoveries"]
        
        return {
            "total_recoveries": total,
            "cache_hits": self.recovery_stats["cache_hits"],
            "cache_hit_rate": self.recovery_stats["cache_hits"] / total if total > 0 else 0,
            "fallback_successes": self.recovery_stats["fallback_successes"],
            "fallback_success_rate": self.recovery_stats["fallback_successes"] / total if total > 0 else 0,
            "degraded_responses": self.recovery_stats["degraded_responses"],
            "degraded_response_rate": self.recovery_stats["degraded_responses"] / total if total > 0 else 0,
            "failed_recoveries": self.recovery_stats["failed_recoveries"]
        }
