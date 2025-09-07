from pydantic import BaseModel, Field
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

# API response structure extends BookingResponse
class ReplyResponse(BookingResponse):
    id: str  # UUID we generate
    created_date: str  # The create time of this reply
