from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from enum import Enum
from datetime import datetime
import uuid

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class ActionType(str, Enum):
    PROPOSE_TOUR = "propose_tour"
    ASK_CLARIFICATION = "ask_clarification"
    HANDOFF_HUMAN = "handoff_human"

class BookingResponse(BaseModel):
    """Core response structure that all prompts return using structured output"""
    reply: str = Field(description="Your conversational reply to send to the customer")
    action: ActionType = Field(default=ActionType.ASK_CLARIFICATION, description="Next action - only set when explicitly needed, defaults to ask_clarification")
    propose_time: Optional[str] = Field(default=None, description="Proposed tour time in ISO format - only set when proposing a tour")

class LeadInfo(BaseModel):
    """Lead information with required fields"""
    name: str = Field(..., min_length=1, description="Lead name is required")
    email: str = Field(..., min_length=1, description="Lead email is required")
    
    @validator('email')
    def validate_email(cls, v):
        if not v or not v.strip():
            raise ValueError('Email cannot be empty')
        if '@' not in v:
            raise ValueError('Email must be a valid email address')
        return v.strip()
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

class ReplyRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Message cannot be empty")
    email_id: Optional[str] = None
    lead: LeadInfo = Field(..., description="Lead information is required")
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

# API response structure extends BookingResponse
class ReplyResponse(BookingResponse):
    id: str  # UUID we generate
    created_date: str  # The create time of this reply
    parent_id: Optional[str] = None  # ID of the user message this is responding to
