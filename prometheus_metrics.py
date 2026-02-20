"""
Phase 4: Prometheus Metrics Integration
Production observability with Prometheus-compatible metrics
"""

from typing import Dict, Optional
from datetime import datetime
from collections import defaultdict
import time

from logging_system import StructuredLogger

logger = StructuredLogger(__name__)


class Counter:
    """Prometheus Counter metric"""
    
    def __init__(self, name: str, description: str, labels: list = None):
        self.name = name
        self.description = description
        self.labels = labels or []
        self.value = 0.0
        self.label_values: Dict[tuple, float] = defaultdict(float)
    
    def inc(self, amount: float = 1.0, label_dict: Optional[Dict] = None):
        """Increment counter"""
        if label_dict:
            key = tuple(label_dict.get(l) for l in self.labels)
            self.label_values[key] += amount
        else:
            self.value += amount
    
    def to_prometheus_format(self) -> str:
        """Format as Prometheus text format"""
        lines = [f"# HELP {self.name} {self.description}"]
        lines.append(f"# TYPE {self.name} counter")
        
        if self.label_values:
            for label_tuple, value in self.label_values.items():
                label_str = ",".join(f"{l}=\"{v}\"" for l, v in zip(self.labels, label_tuple))
                lines.append(f"{self.name}{{{label_str}}} {value}")
        else:
            lines.append(f"{self.name} {self.value}")
        
        return "\n".join(lines)


class Gauge:
    """Prometheus Gauge metric"""
    
    def __init__(self, name: str, description: str, labels: list = None):
        self.name = name
        self.description = description
        self.labels = labels or []
        self.value = 0.0
        self.label_values: Dict[tuple, float] = defaultdict(float)
    
    def set(self, value: float, label_dict: Optional[Dict] = None):
        """Set gauge value"""
        if label_dict:
            key = tuple(label_dict.get(l) for l in self.labels)
            self.label_values[key] = value
        else:
            self.value = value
    
    def inc(self, amount: float = 1.0, label_dict: Optional[Dict] = None):
        """Increment gauge"""
        if label_dict:
            key = tuple(label_dict.get(l) for l in self.labels)
            self.label_values[key] += amount
        else:
            self.value += amount
    
    def dec(self, amount: float = 1.0, label_dict: Optional[Dict] = None):
        """Decrement gauge"""
        if label_dict:
            key = tuple(label_dict.get(l) for l in self.labels)
            self.label_values[key] -= amount
        else:
            self.value -= amount


class Histogram:
    """Prometheus Histogram metric"""
    
    DEFAULT_BUCKETS = [0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0]
    
    def __init__(self, name: str, description: str, buckets: list = None, labels: list = None):
        self.name = name
        self.description = description
        self.buckets = buckets or self.DEFAULT_BUCKETS
        self.labels = labels or []
        self.observations: Dict[tuple, list] = defaultdict(list)
    
    def observe(self, value: float, label_dict: Optional[Dict] = None):
        """Record observation"""
        if label_dict:
            key = tuple(label_dict.get(l) for l in self.labels)
            self.observations[key].append(value)
        else:
            self.observations[()].append(value)
        
        logger.debug("Histogram observation", name=self.name, value=value)
    
    def get_bucket_counts(self, label_dict: Optional[Dict] = None) -> Dict[float, int]:
        """Get bucket counts"""
        key = tuple(label_dict.get(l) for l in self.labels) if label_dict else ()
        observations = self.observations.get(key, [])
        
        buckets = {}
        for bucket in self.buckets:
            buckets[bucket] = sum(1 for obs in observations if obs <= bucket)
        return buckets
    
    def get_sum(self, label_dict: Optional[Dict] = None) -> float:
        """Get sum of observations"""
        key = tuple(label_dict.get(l) for l in self.labels) if label_dict else ()
        return sum(self.observations.get(key, []))


class PrometheusRegistry:
    """Registry for all metrics"""
    
    def __init__(self):
        self.metrics: Dict[str, object] = {}
    
    def counter(self, name: str, description: str, labels: list = None) -> Counter:
        """Create or get counter"""
        if name not in self.metrics:
            self.metrics[name] = Counter(name, description, labels)
        return self.metrics[name]
    
    def gauge(self, name: str, description: str, labels: list = None) -> Gauge:
        """Create or get gauge"""
        if name not in self.metrics:
            self.metrics[name] = Gauge(name, description, labels)
        return self.metrics[name]
    
    def histogram(self, name: str, description: str, buckets: list = None, labels: list = None) -> Histogram:
        """Create or get histogram"""
        if name not in self.metrics:
            self.metrics[name] = Histogram(name, description, buckets, labels)
        return self.metrics[name]
    
    def export_prometheus(self) -> str:
        """Export all metrics in Prometheus format"""
        output = []
        for metric in self.metrics.values():
            output.append(metric.to_prometheus_format())
        return "\n\n".join(output)


class MetricsCollector:
    """Collect application metrics"""
    
    def __init__(self):
        self.registry = PrometheusRegistry()
        
        self.request_count = self.registry.counter(
            "http_requests_total",
            "Total HTTP requests",
            labels=["method", "endpoint", "status"]
        )
        
        self.request_duration = self.registry.histogram(
            "http_request_duration_seconds",
            "HTTP request latency",
            labels=["method", "endpoint"]
        )
        
        self.active_requests = self.registry.gauge(
            "http_requests_active",
            "Active HTTP requests",
            labels=["method", "endpoint"]
        )
        
        self.function_calls = self.registry.counter(
            "function_calls_total",
            "Total function calls",
            labels=["function", "status"]
        )
        
        self.function_duration = self.registry.histogram(
            "function_duration_seconds",
            "Function execution time",
            labels=["function"]
        )
        
        self.cache_hits = self.registry.counter(
            "cache_hits_total",
            "Cache hits"
        )
        
        self.cache_misses = self.registry.counter(
            "cache_misses_total",
            "Cache misses"
        )
        
        self.errors_total = self.registry.counter(
            "errors_total",
            "Total errors",
            labels=["type"]
        )
    
    def record_request(self, method: str, endpoint: str, status_code: int, duration_ms: float):
        """Record HTTP request metrics"""
        self.request_count.inc(
            label_dict={"method": method, "endpoint": endpoint, "status": str(status_code)}
        )
        self.request_duration.observe(
            duration_ms / 1000.0,
            label_dict={"method": method, "endpoint": endpoint}
        )
    
    def record_function_call(self, function: str, success: bool, duration_ms: float):
        """Record function call metrics"""
        status = "success" if success else "failure"
        self.function_calls.inc(label_dict={"function": function, "status": status})
        self.function_duration.observe(
            duration_ms / 1000.0,
            label_dict={"function": function}
        )
    
    def record_error(self, error_type: str):
        """Record error metrics"""
        self.errors_total.inc(label_dict={"type": error_type})
    
    def export_metrics(self) -> str:
        """Export all metrics"""
        return self.registry.export_prometheus()


global_metrics = MetricsCollector()
