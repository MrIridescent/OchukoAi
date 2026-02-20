"""
Phase 3: Prompt Injection Detection & JWT Security
Protects LLM from prompt injection attacks + API authentication
"""

import jwt
import os
import re
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from functools import wraps
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthCredentials
import hashlib

from logging_system import StructuredLogger

logger = StructuredLogger(__name__)

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


class JWTManager:
    """JWT token generation and validation"""
    
    @staticmethod
    def create_token(user_id: str, metadata: Optional[Dict] = None) -> str:
        """Create JWT token with expiration"""
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
            "iat": datetime.utcnow(),
            "metadata": metadata or {}
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        logger.info("JWT token created", user_id=user_id)
        return token
    
    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token")
            raise HTTPException(status_code=401, detail="Invalid token")


class PromptInjectionDetector:
    """Detect prompt injection attacks in LLM inputs"""
    
    INJECTION_PATTERNS = [
        r"(?i)(ignore|disregard|forget).+(previous|prior|above).+(instruction|prompt|command)",
        r"(?i)(treat|act).+as.+(system|admin|root|developer)",
        r"(?i)(execute|run|perform).+(code|script|command)",
        r"(?i)(tell|show|reveal).+(me|us).+(your|the).+(prompt|instruction|system|secret)",
        r"(?i)(\n\s*){2,}(System:|Instruction:|Prompt:|Admin:|Root:|Internal:)",
        r"(?i)<prompt>.*?</prompt>",
        r"(?i)\{\{.*?\}\}",
        r"(?i)__.*?__",
    ]
    
    SUSPICIOUS_KEYWORDS = [
        "system prompt", "ignore previous", "disregard previous", "forget about",
        "execute code", "run command", "sql injection", "jailbreak",
        "hidden instruction", "secret prompt", "internal memo",
    ]
    
    @classmethod
    def detect_injection(cls, text: str) -> Dict[str, Any]:
        """Detect prompt injection attempts"""
        score = 0.0
        detected_patterns = []
        
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, text):
                score += 0.3
                detected_patterns.append(pattern[:30])
        
        text_lower = text.lower()
        for keyword in cls.SUSPICIOUS_KEYWORDS:
            if keyword in text_lower:
                score += 0.2
        
        score = min(score, 1.0)
        is_injection = score >= 0.5
        
        if is_injection:
            logger.warning(
                "Prompt injection detected",
                score=score,
                patterns=detected_patterns[:3]
            )
        
        return {
            "is_injection": is_injection,
            "risk_score": score,
            "detected_patterns": detected_patterns,
            "original_length": len(text),
        }
    
    @classmethod
    def sanitize(cls, text: str) -> str:
        """Sanitize text by removing suspicious patterns"""
        sanitized = text
        
        for pattern in cls.INJECTION_PATTERNS:
            sanitized = re.sub(pattern, "[REDACTED]", sanitized, flags=re.IGNORECASE)
        
        logger.debug("Text sanitized", original_len=len(text), sanitized_len=len(sanitized))
        return sanitized


class APIKeyManager:
    """Manage API keys for service-to-service authentication"""
    
    @staticmethod
    def hash_key(key: str) -> str:
        """Hash API key for storage"""
        return hashlib.sha256(key.encode()).hexdigest()
    
    @staticmethod
    def verify_key(provided_key: str, stored_hash: str) -> bool:
        """Verify provided key against hash"""
        return APIKeyManager.hash_key(provided_key) == stored_hash


class SecurityMiddleware:
    """Security layer for all requests"""
    
    def __init__(self):
        self.jwt_manager = JWTManager()
        self.injection_detector = PromptInjectionDetector()
    
    async def verify_auth(self, credentials: Optional[HTTPAuthCredentials]) -> Dict[str, Any]:
        """Verify authentication credentials"""
        if not credentials:
            raise HTTPException(status_code=401, detail="Missing authentication")
        
        return self.jwt_manager.verify_token(credentials.credentials)
    
    async def check_injection_risk(self, content: str) -> Dict[str, Any]:
        """Check for prompt injection in content"""
        return self.injection_detector.detect_injection(content)


def require_auth(func):
    """Decorator to require authentication"""
    @wraps(func)
    async def wrapper(*args, request: Request, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
        
        token = auth_header.split(" ")[1]
        payload = JWTManager.verify_token(token)
        
        return await func(*args, user_id=payload["user_id"], **kwargs)
    
    return wrapper


def check_injection(func):
    """Decorator to check for prompt injection"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        content = kwargs.get("content") or (args[0] if args else "")
        detection = PromptInjectionDetector.detect_injection(str(content))
        
        if detection["is_injection"]:
            raise HTTPException(
                status_code=400,
                detail=f"Potential prompt injection detected (risk: {detection['risk_score']:.2f})"
            )
        
        return await func(*args, **kwargs)
    
    return wrapper
