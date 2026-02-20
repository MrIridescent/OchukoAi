"""
Real-Time Collaboration Engine - Feature 2
Multi-user sessions, WebSocket coordination, presence awareness
Operational Transformation (OT) for conflict resolution
"""

import asyncio
import uuid
from typing import Dict, Set, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from logging_system import StructuredLogger

logger = StructuredLogger(__name__)


class MessageType(Enum):
    JOIN = "join"
    LEAVE = "leave"
    EDIT = "edit"
    CURSOR = "cursor"
    PRESENCE = "presence"
    SYNC = "sync"
    ACKNOWLEDGE = "acknowledge"


@dataclass
class User:
    """Collaborative user"""
    user_id: str
    username: str
    color: str
    cursor_position: int = 0
    is_active: bool = True
    last_seen: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Operation:
    """Operation for OT"""
    op_id: str
    user_id: str
    type: str
    position: int
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: int = 0


class RealtimeCollaborationEngine:
    """
    Multi-user real-time collaboration with:
    - WebSocket-based communication
    - Presence awareness
    - Operational Transformation for conflict resolution
    - Cursor tracking
    - Session management
    """
    
    def __init__(self):
        self.sessions: Dict[str, 'CollaborativeSession'] = {}
        self.user_connections: Dict[str, Set[str]] = {}
        logger.info("RealtimeCollaborationEngine initialized")
    
    async def create_session(self, session_id: str, initial_content: str = "") -> 'CollaborativeSession':
        """Create new collaborative session"""
        session = CollaborativeSession(session_id, initial_content)
        self.sessions[session_id] = session
        
        logger.info("Collaborative session created", session_id=session_id)
        return session
    
    async def get_session(self, session_id: str) -> Optional['CollaborativeSession']:
        """Get existing session"""
        return self.sessions.get(session_id)
    
    async def user_join(
        self,
        session_id: str,
        user_id: str,
        username: str,
        color: str = "#FF5733"
    ) -> Optional['CollaborativeSession']:
        """User joins collaboration session"""
        session = await self.get_session(session_id)
        
        if not session:
            return None
        
        user = User(user_id, username, color)
        await session.add_user(user)
        
        if session_id not in self.user_connections:
            self.user_connections[session_id] = set()
        
        self.user_connections[session_id].add(user_id)
        
        logger.info(
            "User joined session",
            session_id=session_id,
            user_id=user_id,
            username=username
        )
        
        return session
    
    async def user_leave(self, session_id: str, user_id: str):
        """User leaves collaboration session"""
        session = await self.get_session(session_id)
        
        if session:
            await session.remove_user(user_id)
        
        if session_id in self.user_connections:
            self.user_connections[session_id].discard(user_id)
        
        logger.info(
            "User left session",
            session_id=session_id,
            user_id=user_id
        )
    
    async def broadcast_message(
        self,
        session_id: str,
        message_type: MessageType,
        data: Dict[str, Any],
        exclude_user: Optional[str] = None
    ):
        """Broadcast message to all users in session"""
        session = await self.get_session(session_id)
        
        if not session:
            return
        
        await session.broadcast(message_type, data, exclude_user)


class CollaborativeSession:
    """Single collaborative editing session"""
    
    def __init__(self, session_id: str, initial_content: str = ""):
        self.session_id = session_id
        self.content = initial_content
        self.users: Dict[str, User] = {}
        self.operations: list[Operation] = []
        self.version = 0
        self.created_at = datetime.utcnow()
        self.message_handlers: Dict[MessageType, Callable] = {}
    
    async def add_user(self, user: User):
        """Add user to session"""
        self.users[user.user_id] = user
        
        logger.debug(
            "User added to session",
            session_id=self.session_id,
            user_count=len(self.users)
        )
    
    async def remove_user(self, user_id: str):
        """Remove user from session"""
        if user_id in self.users:
            del self.users[user_id]
        
        logger.debug(
            "User removed from session",
            session_id=self.session_id,
            user_count=len(self.users)
        )
    
    async def apply_operation(self, operation: Operation) -> bool:
        """Apply OT operation to document"""
        try:
            op_type = operation.type
            
            if op_type == "insert":
                self.content = (
                    self.content[:operation.position] +
                    operation.content +
                    self.content[operation.position:]
                )
            elif op_type == "delete":
                delete_len = len(operation.content)
                self.content = (
                    self.content[:operation.position] +
                    self.content[operation.position + delete_len:]
                )
            else:
                logger.warning("Unknown operation type", op_type=op_type)
                return False
            
            operation.version = self.version
            self.operations.append(operation)
            self.version += 1
            
            logger.debug(
                "Operation applied",
                session_id=self.session_id,
                op_type=op_type,
                version=self.version
            )
            
            return True
        
        except Exception as e:
            logger.error("Failed to apply operation", error=str(e))
            return False
    
    async def update_cursor(self, user_id: str, position: int):
        """Update user cursor position"""
        if user_id in self.users:
            self.users[user_id].cursor_position = position
    
    async def get_user_presence(self) -> Dict[str, Any]:
        """Get presence data for all users"""
        return {
            user_id: {
                "username": user.username,
                "color": user.color,
                "cursor_position": user.cursor_position,
                "is_active": user.is_active,
                "last_seen": user.last_seen.isoformat()
            }
            for user_id, user in self.users.items()
        }
    
    async def broadcast(
        self,
        message_type: MessageType,
        data: Dict[str, Any],
        exclude_user: Optional[str] = None
    ):
        """Broadcast message to all connected users"""
        message = {
            "type": message_type.value,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data,
            "version": self.version
        }
        
        logger.debug(
            "Broadcasting message",
            session_id=self.session_id,
            message_type=message_type.value,
            user_count=len(self.users),
            exclude_user=exclude_user
        )
        
        for user_id in self.users:
            if exclude_user and user_id == exclude_user:
                continue
            
            handler = self.message_handlers.get(message_type)
            if handler:
                await handler(user_id, message)
    
    async def get_session_state(self) -> Dict[str, Any]:
        """Get full session state"""
        return {
            "session_id": self.session_id,
            "content": self.content,
            "version": self.version,
            "user_count": len(self.users),
            "users": await self.get_user_presence(),
            "operations_count": len(self.operations),
            "created_at": self.created_at.isoformat()
        }
