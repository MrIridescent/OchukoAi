"""
OpenTelemetry Distributed Tracing
Full observability with spans, metrics, and logs
Cross-service tracing with correlation IDs
"""

from typing import Optional, Dict, Any, Callable
from datetime import datetime
from functools import wraps
import asyncio
from enum import Enum

from logging_system import StructuredLogger, set_request_context, get_request_context

logger = StructuredLogger(__name__)


class SpanKind(Enum):
    """OpenTelemetry span kinds"""
    INTERNAL = "internal"
    SERVER = "server"
    CLIENT = "client"
    PRODUCER = "producer"
    CONSUMER = "consumer"


class Span:
    """Distributed tracing span"""
    
    def __init__(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        parent_span_id: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None
    ):
        self.name = name
        self.kind = kind
        self.span_id = str(datetime.utcnow().timestamp())
        self.parent_span_id = parent_span_id
        self.attributes = attributes or {}
        self.start_time = datetime.utcnow()
        self.end_time: Optional[datetime] = None
        self.events: list = []
        self.status = "unset"
        self.error: Optional[str] = None
    
    def add_event(self, event_name: str, attributes: Optional[Dict] = None):
        """Add event to span"""
        self.events.append({
            "name": event_name,
            "timestamp": datetime.utcnow().isoformat(),
            "attributes": attributes or {}
        })
    
    def set_attribute(self, key: str, value: Any):
        """Set span attribute"""
        self.attributes[key] = value
    
    def set_status(self, status: str, description: Optional[str] = None):
        """Set span status"""
        self.status = status
        if description:
            self.error = description
    
    def end(self):
        """End span"""
        self.end_time = datetime.utcnow()
        duration_ms = (self.end_time - self.start_time).total_seconds() * 1000
        
        logger.debug(
            f"Span ended: {self.name}",
            span_id=self.span_id,
            duration_ms=duration_ms,
            status=self.status,
            kind=self.kind.value
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert span to dictionary"""
        return {
            "name": self.name,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "kind": self.kind.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": (self.end_time - self.start_time).total_seconds() * 1000 if self.end_time else None,
            "status": self.status,
            "error": self.error,
            "attributes": self.attributes,
            "events": self.events,
            "context": get_request_context()
        }


class TracingContext:
    """Context for distributed tracing"""
    
    def __init__(self, trace_id: str, span_id: Optional[str] = None):
        self.trace_id = trace_id
        self.parent_span_id = span_id
        self.spans: Dict[str, Span] = {}
    
    def create_span(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        attributes: Optional[Dict] = None
    ) -> Span:
        """Create child span"""
        span = Span(
            name=name,
            kind=kind,
            parent_span_id=self.parent_span_id,
            attributes=attributes
        )
        self.spans[span.span_id] = span
        return span
    
    def get_trace_summary(self) -> Dict[str, Any]:
        """Get trace summary"""
        return {
            "trace_id": self.trace_id,
            "span_count": len(self.spans),
            "spans": [span.to_dict() for span in self.spans.values()],
            "total_duration_ms": sum(
                (span.end_time - span.start_time).total_seconds() * 1000
                for span in self.spans.values() if span.end_time
            )
        }


class ObservabilitySystem:
    """
    Complete observability system with:
    - Distributed tracing (OpenTelemetry)
    - Request context propagation
    - Span tracking
    - Error tracking
    - Performance metrics
    """
    
    def __init__(self):
        self.traces: Dict[str, TracingContext] = {}
        self.metrics: Dict[str, Any] = {
            "total_requests": 0,
            "total_errors": 0,
            "total_duration_ms": 0,
            "average_latency_ms": 0
        }
        logger.info("ObservabilitySystem initialized")
    
    async def start_trace(self, trace_id: str) -> TracingContext:
        """Start new distributed trace"""
        context = TracingContext(trace_id)
        self.traces[trace_id] = context
        
        logger.debug(f"Trace started: {trace_id}")
        return context
    
    async def end_trace(self, trace_id: str) -> Dict[str, Any]:
        """End trace and get summary"""
        context = self.traces.get(trace_id)
        
        if not context:
            return {"error": "Trace not found"}
        
        summary = context.get_trace_summary()
        
        self.metrics["total_requests"] += 1
        self.metrics["total_duration_ms"] += summary["total_duration_ms"]
        self.metrics["average_latency_ms"] = (
            self.metrics["total_duration_ms"] / self.metrics["total_requests"]
        )
        
        logger.info(
            f"Trace ended: {trace_id}",
            span_count=summary["span_count"],
            duration_ms=summary["total_duration_ms"]
        )
        
        return summary
    
    def trace_function(self, name: str, kind: SpanKind = SpanKind.INTERNAL):
        """Decorator to trace function execution"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                trace_id = get_request_context().get("request_id")
                
                if not trace_id:
                    trace_id = str(datetime.utcnow().timestamp())
                
                context = await self.start_trace(trace_id)
                span = context.create_span(name, kind)
                
                try:
                    result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
                    span.set_status("ok")
                    return result
                except Exception as e:
                    span.set_status("error", str(e))
                    self.metrics["total_errors"] += 1
                    raise
                finally:
                    span.end()
                    await self.end_trace(trace_id)
            
            return async_wrapper
        
        return decorator
    
    async def get_observability_metrics(self) -> Dict[str, Any]:
        """Get observability metrics"""
        error_rate = (
            self.metrics["total_errors"] / self.metrics["total_requests"]
            if self.metrics["total_requests"] > 0 else 0
        )
        
        return {
            "total_requests": self.metrics["total_requests"],
            "total_errors": self.metrics["total_errors"],
            "error_rate": error_rate,
            "average_latency_ms": self.metrics["average_latency_ms"],
            "total_traced_duration_ms": self.metrics["total_duration_ms"],
            "active_traces": len(self.traces)
        }
