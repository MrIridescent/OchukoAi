"""
Backend Configuration Module
Loads and manages environment variables and application settings
"""

import os
from typing import List
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""
    
    # Environment
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    WORKERS: int = int(os.getenv("WORKERS", 4))
    
    # LLM APIs
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", 2048))
    
    CLAUDE_API_KEY: str = os.getenv("CLAUDE_API_KEY", "")
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")
    
    USE_LOCAL_LLM: bool = os.getenv("USE_LOCAL_LLM", "false").lower() == "true"
    LOCAL_MODEL_PATH: str = os.getenv("LOCAL_MODEL_PATH", "/models/llama2")
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/jarvis"
    )
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/jarvis")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # AI Features
    ENABLE_VOICE: bool = os.getenv("ENABLE_VOICE", "true").lower() == "true"
    ENABLE_FACE_RECOGNITION: bool = os.getenv("ENABLE_FACE_RECOGNITION", "true").lower() == "true"
    ENABLE_EMOTION_DETECTION: bool = os.getenv("ENABLE_EMOTION_DETECTION", "true").lower() == "true"
    ENABLE_LEARNING: bool = os.getenv("ENABLE_LEARNING", "true").lower() == "true"
    ENABLE_THINKING: bool = os.getenv("ENABLE_THINKING", "true").lower() == "true"
    ENABLE_TASK_EXECUTION: bool = os.getenv("ENABLE_TASK_EXECUTION", "true").lower() == "true"
    
    # Speech
    SPEECH_PROVIDER: str = os.getenv("SPEECH_PROVIDER", "google")
    GOOGLE_CLOUD_API_KEY: str = os.getenv("GOOGLE_CLOUD_API_KEY", "")
    TTS_PROVIDER: str = os.getenv("TTS_PROVIDER", "google")
    
    # Face Recognition
    FACE_RECOGNITION_THRESHOLD: float = float(os.getenv("FACE_RECOGNITION_THRESHOLD", 0.6))
    EMOTION_DETECTION_THRESHOLD: float = float(os.getenv("EMOTION_DETECTION_THRESHOLD", 0.7))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", 24))
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000"
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", 100))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", 60))
    
    # Storage
    STORAGE_TYPE: str = os.getenv("STORAGE_TYPE", "local")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    
    # AWS S3
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_S3_BUCKET: str = os.getenv("AWS_S3_BUCKET", "jarvis-ai")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    
    # Monitoring
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    LOG_FILE: str = os.getenv("LOG_FILE", "/var/log/jarvis/app.log")
    PROMETHEUS_METRICS: bool = os.getenv("PROMETHEUS_METRICS", "true").lower() == "true"
    
    # Development
    HOT_RELOAD: bool = os.getenv("HOT_RELOAD", "true").lower() == "true"
    MOCK_RESPONSES: bool = os.getenv("MOCK_RESPONSES", "false").lower() == "true"
    SIMULATE_VOICE: bool = os.getenv("SIMULATE_VOICE", "false").lower() == "true"
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Quick access
settings = get_settings()
