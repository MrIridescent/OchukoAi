"""
Comprehensive request validation schemas
Uses Pydantic v2 for runtime validation
"""

from pydantic import BaseModel, Field, validator, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class TextProcessRequest(BaseModel):
    """Validate text processing requests"""
    user_id: str = Field(..., min_length=1, max_length=255)
    query: str = Field(..., min_length=1, max_length=10000)
    context: Optional[str] = Field("general", max_length=100)
    observations: Optional[List[str]] = Field(default_factory=list, max_items=50)
    conversation_history: Optional[List[Dict[str, str]]] = Field(default_factory=list, max_items=100)
    credentials: Optional[Dict[str, str]] = Field(default_factory=dict)
    ip: Optional[str] = Field("", max_length=50)
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "query": "What is machine learning?",
                "context": "educational",
                "observations": ["asked_before"],
                "conversation_history": []
            }
        }


class MediaProcessRequest(BaseModel):
    """Validate media processing requests"""
    user_id: str = Field(..., min_length=1)
    file_type: str = Field(..., pattern="^(image|audio|video)$")
    file_url: Optional[str] = Field(None, max_length=2000)
    mode: str = Field("analyze", pattern="^(analyze|summarize|extract)$")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "file_type": "image",
                "mode": "analyze"
            }
        }


class HealthCheckResponse(BaseModel):
    """Response for health check endpoint"""
    status: str = Field(..., pattern="^(healthy|degraded|unhealthy)$")
    timestamp: datetime
    version: str
    uptime_seconds: float
    subsystems: Dict[str, str] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2026-02-20T18:30:00",
                "version": "5.1.0",
                "uptime_seconds": 3600.5,
                "subsystems": {
                    "database": "healthy",
                    "cache": "healthy",
                    "ai_models": "healthy"
                }
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    message: str
    error_id: str
    request_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "VALIDATION_ERROR",
                "message": "Invalid user_id format",
                "error_id": "err_12345",
                "request_id": "req_98765"
            }
        }


class ProcessTextResponse(BaseModel):
    """Response from text processing"""
    request_id: str
    user_id: str
    response: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: Optional[str] = None
    processing_time_ms: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "request_id": "req_123",
                "user_id": "user123",
                "response": "Machine learning is...",
                "confidence": 0.95,
                "processing_time_ms": 245.3
            }
        }
