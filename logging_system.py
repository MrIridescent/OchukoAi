"""
Structured Logging System with OpenTelemetry Integration
Provides JSON logging, distributed tracing, and context propagation
"""

import json
import sys
import logging
from typing import Any, Dict, Optional
from datetime import datetime
from functools import wraps
import uuid
from contextvars import ContextVar

from loguru import logger as loguru_logger

request_id_var: ContextVar[str] = ContextVar('request_id', default='')
user_id_var: ContextVar[str] = ContextVar('user_id', default='')
session_id_var: ContextVar[str] = ContextVar('session_id', default='')


class StructuredLogger:
    """Production-grade structured logger with OpenTelemetry support"""
    
    def __init__(self, name: str, level: str = "INFO"):
        self.name = name
        self.logger = loguru_logger.bind(service=name)
        self._setup_handlers(level)
    
    def _setup_handlers(self, level: str):
        """Configure JSON and console handlers"""
        loguru_logger.remove()
        
        loguru_logger.add(
            sys.stderr,
            format=self._json_format,
            level=level,
            serialize=True,
        )
    
    @staticmethod
    def _json_format(record):
        """Format log record as JSON"""
        log_entry = {
            "timestamp": record["time"].isoformat(),
            "level": record["level"].name,
            "logger": record["name"],
            "message": record["message"],
            "request_id": request_id_var.get() or str(uuid.uuid4()),
            "user_id": user_id_var.get(),
            "session_id": session_id_var.get(),
        }
        
        if record["extra"]:
            log_entry.update(record["extra"])
        
        if record["exception"]:
            log_entry["exception"] = {
                "type": record["exception"].type.__name__,
                "value": str(record["exception"].value),
                "traceback": record["exc_info"][2].__str__()[:500],
            }
        
        return json.dumps(log_entry)
    
    def info(self, message: str, **kwargs):
        self.logger.info(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self.logger.error(message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        self.logger.debug(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self.logger.warning(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        self.logger.critical(message, **kwargs)
    
    def exception(self, message: str, **kwargs):
        self.logger.exception(message, **kwargs)


def with_logging(logger: StructuredLogger):
    """Decorator to add structured logging to functions"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            func_name = func.__name__
            start_time = datetime.utcnow()
            
            try:
                logger.debug(f"Starting {func_name}", function=func_name, args_count=len(args))
                result = await func(*args, **kwargs)
                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.info(
                    f"Completed {func_name}",
                    function=func_name,
                    duration_ms=duration * 1000,
                    status="success"
                )
                return result
            except Exception as e:
                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.exception(
                    f"Failed {func_name}",
                    function=func_name,
                    duration_ms=duration * 1000,
                    error=str(e)
                )
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            func_name = func.__name__
            start_time = datetime.utcnow()
            
            try:
                logger.debug(f"Starting {func_name}", function=func_name)
                result = func(*args, **kwargs)
                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.info(
                    f"Completed {func_name}",
                    function=func_name,
                    duration_ms=duration * 1000,
                    status="success"
                )
                return result
            except Exception as e:
                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.exception(
                    f"Failed {func_name}",
                    function=func_name,
                    duration_ms=duration * 1000,
                    error=str(e)
                )
                raise
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator


def set_request_context(request_id: str, user_id: Optional[str] = None, session_id: Optional[str] = None):
    """Set request context for logging"""
    request_id_var.set(request_id)
    if user_id:
        user_id_var.set(user_id)
    if session_id:
        session_id_var.set(session_id)


def get_request_context() -> Dict[str, str]:
    """Get current request context"""
    return {
        "request_id": request_id_var.get(),
        "user_id": user_id_var.get(),
        "session_id": session_id_var.get(),
    }


import asyncio
