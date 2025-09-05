from pydantic import BaseModel
from typing import Optional, Dict, Any
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class ReplyRequest(BaseModel):
    message: str
    email_id: Optional[str] = None
    lead: Optional[Dict[str, Any]] = None
    preferences: Optional[Dict[str, Any]] = None
    community_id: Optional[str] = None

class MessageContent(BaseModel):
    role: MessageRole
    content: str

class CreateMessageData(BaseModel):
    """Data needed to create a new message"""
    role: MessageRole
    content: str
    email_id: Optional[str] = None
    parent_id: Optional[str] = None

class MessageData(BaseModel):
    """Complete message data from database"""
    id: str  # UUID as string
    message: MessageContent
    created_date: str

class ReplyResponse(BaseModel):
    message: MessageData
