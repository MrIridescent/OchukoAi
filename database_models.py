"""
SQLAlchemy ORM models with base configuration
Ready for Alembic migrations
"""

from sqlalchemy import Column, String, DateTime, Integer, Float, Boolean, Text, JSON, ForeignKey, Index, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from datetime import datetime
import uuid
import os

Base = declarative_base()


class User(Base):
    """User profile and settings"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    last_active = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    interactions = relationship("Interaction", back_populates="user", cascade="all, delete-orphan")
    __table_args__ = (Index('idx_user_email', 'email'), Index('idx_user_username', 'username'))


class Interaction(Base):
    """User interaction/conversation log"""
    __tablename__ = "interactions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    request_id = Column(String(36), nullable=False, unique=True, index=True)
    input_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=True)
    response_confidence = Column(Float, default=0.0)
    processing_time_ms = Column(Float, nullable=False)
    error = Column(String(500), nullable=True)
    status = Column(String(50), default="success", nullable=False)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    user = relationship("User", back_populates="interactions")
    __table_args__ = (Index('idx_interaction_user', 'user_id'), Index('idx_interaction_created', 'created_at'))


class Session(Base):
    """User session tracking"""
    __tablename__ = "sessions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    started_at = Column(DateTime, server_default=func.now(), nullable=False)
    last_active = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    ended_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    __table_args__ = (Index('idx_session_user', 'user_id'), Index('idx_session_token', 'session_token'))


class ModelCache(Base):
    """Cache for model outputs and expensive computations"""
    __tablename__ = "model_cache"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cache_key = Column(String(255), unique=True, nullable=False, index=True)
    input_hash = Column(String(64), nullable=False, index=True)
    output = Column(JSON, nullable=False)
    model_version = Column(String(50), nullable=False)
    hit_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)
    
    __table_args__ = (Index('idx_cache_key', 'cache_key'), Index('idx_cache_expires', 'expires_at'))


def get_db_engine():
    """Get SQLAlchemy engine from environment"""
    database_url = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    return create_engine(database_url, echo=False, pool_pre_ping=True)


def init_db():
    """Initialize database with all tables"""
    engine = get_db_engine()
    Base.metadata.create_all(bind=engine)
    return engine
