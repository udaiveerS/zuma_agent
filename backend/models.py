from sqlalchemy import Column, String, DateTime, Boolean, Enum, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid
import enum

Base = declarative_base()

class StepEnum(enum.Enum):
    """Enum for tracking which prompt step the message belongs to"""
    INITIAL = "initial"
    CONTEXT = "context"
    REASONING = "reasoning"
    RESPONSE = "response"
    FOLLOWUP = "followup"

class Message(Base):
    __tablename__ = "messages"

    # UUIDv4 primary key for external ID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # JSONB for flexible message data (role, content, raw stuff)
    message = Column(JSONB, nullable=False)
    
    # Role duplicated as separate column for fast filtering
    role = Column(String(20), nullable=False, index=True)
    
    # Visibility control
    visible_to_user = Column(Boolean, default=True, nullable=False, index=True)
    
    # Step tracking for prompt workflow
    step_id = Column(Enum(StepEnum), nullable=True, index=True)
    
    # Parent message linking
    parent_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    
    # User linking (foreign key to users table)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=True, index=True)
    
    # Timestamp
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def to_dict(self):
        return {
            "id": str(self.id),  # Convert UUID to string for JSON serialization
            "message": self.message,
            "role": self.role,
            "visible_to_user": self.visible_to_user,
            "step_id": self.step_id.value if self.step_id else None,
            "parent_id": str(self.parent_id) if self.parent_id else None,
            "user_id": str(self.user_id) if self.user_id else None,
            "created_date": self.created_date.isoformat() if self.created_date else None
        }

    @property
    def content(self):
        """Helper property to get content from JSON message"""
        return self.message.get('content') if self.message else None


class User(Base):
    """User model matching existing users table schema"""
    __tablename__ = "users"

    # Primary key matching existing schema
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # User identification
    email = Column(Text, unique=True, nullable=False, index=True)
    name = Column(Text, nullable=True)
    
    # Flexible preferences storage as JSONB
    preferences = Column(JSONB, nullable=True, default=dict)
    
    # Timestamp matching existing schema
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def to_dict(self):
        """Convert user to dictionary for JSON serialization"""
        return {
            "user_id": str(self.user_id),
            "email": self.email,
            "name": self.name,
            "preferences": self.preferences or {},
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def update_preferences(self, new_preferences: dict):
        """Update user preferences by merging with existing"""
        if self.preferences is None:
            self.preferences = {}
        self.preferences = {**self.preferences, **new_preferences}
