"""
Simple database query functions for the Chat API.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
from models import Message

class MessageQueries:
    """Simple message query functions"""
    
    @staticmethod
    def get_recent_messages(db: Session, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent messages ordered by creation date"""
        messages = db.query(Message).order_by(desc(Message.created_date)).limit(limit).all()
        return [msg.to_dict() for msg in messages]