"""
Comprehensive Error Handling System
Global error boundaries, graceful degradation, error recovery
"""

import traceback
import uuid
from typing import Optional, Callable, Any
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from functools import wraps
import asyncio

from logging_system import StructuredLogger, set_request_context, get_request_context

logger = StructuredLogger(__name__)


class ApplicationError(Exception):
    """Base application error with context"""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = 500, context: dict = None):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.context = context or {}
        self.error_id = str(uuid.uuid4())
        super().__init__(self.message)


class ValidationError(ApplicationError):
    """Data validation error"""
    def __init__(self, message: str, field: str = "", context: dict = None):
        super().__init__(message, "VALIDATION_ERROR", 400, context or {})
        self.field = field
        self.context["field"] = field


class ExternalServiceError(ApplicationError):
    """Error calling external service (API, DB, etc)"""
    def __init__(self, service: str, message: str, context: dict = None):
        super().__init__(
            f"Failed to call {service}: {message}",
            "EXTERNAL_SERVICE_ERROR",
            503,
            context or {}
        )
        self.service = service
        self.context["service"] = service


class RateLimitError(ApplicationError):
    """Rate limit exceeded"""
    def __init__(self, limit: int, context: dict = None):
        super().__init__(
            f"Rate limit exceeded: {limit} requests",
            "RATE_LIMIT_ERROR",
            429,
            context or {}
        )
        self.limit = limit


def setup_error_handlers(app: FastAPI):
    """Setup global error handlers for FastAPI app"""
    
    @app.middleware("http")
    async def add_request_id_middleware(request: Request, call_next):
        """Add request ID and context to all requests"""
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        user_id = request.headers.get("X-User-ID", "")
        session_id = request.headers.get("X-Session-ID", "")
        
        set_request_context(request_id, user_id, session_id)
        
        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as e:
            logger.exception("Unhandled exception in request", path=request.url.path, method=request.method)
            return JSONResponse(
                status_code=500,
                content={
                    "error": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred",
                    "request_id": request_id,
                    "error_id": str(uuid.uuid4()),
                }
            )
    
    @app.exception_handler(ApplicationError)
    async def application_error_handler(request: Request, exc: ApplicationError):
        """Handle application errors"""
        logger.error(
            exc.message,
            code=exc.code,
            error_id=exc.error_id,
            status_code=exc.status_code,
            context=exc.context
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.code,
                "message": exc.message,
                "error_id": exc.error_id,
                "request_id": get_request_context().get("request_id"),
                "context": exc.context,
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all unexpected exceptions"""
        error_id = str(uuid.uuid4())
        logger.exception(
            "Unhandled exception",
            error_id=error_id,
            error_type=type(exc).__name__,
            path=request.url.path,
            method=request.method,
            traceback=traceback.format_exc()[:500]
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "error_id": error_id,
                "request_id": get_request_context().get("request_id"),
            }
        )


def with_error_handling(func: Callable) -> Callable:
    """Decorator to add error handling to async functions"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ApplicationError:
            raise
        except Exception as e:
            logger.exception(
                f"Error in {func.__name__}",
                error_type=type(e).__name__,
                error=str(e)
            )
            raise ApplicationError(
                f"Operation failed: {str(e)}",
                "OPERATION_FAILED",
                500
            )
    return wrapper


class CircuitBreaker:
    """Circuit breaker pattern for external service calls"""
    def __init__(self, name: str, failure_threshold: int = 5, timeout: int = 60):
        self.name = name
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker"""
        if self.is_open:
            if (datetime.utcnow() - self.last_failure_time).total_seconds() > self.timeout:
                logger.info(f"Circuit breaker {self.name} reset", service=self.name)
                self.is_open = False
                self.failure_count = 0
            else:
                raise ExternalServiceError(self.name, "Circuit breaker is open")
        
        try:
            result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.utcnow()
            
            if self.failure_count >= self.failure_threshold:
                self.is_open = True
                logger.error(
                    f"Circuit breaker {self.name} opened",
                    service=self.name,
                    failure_count=self.failure_count
                )
            
            raise ExternalServiceError(self.name, str(e))
