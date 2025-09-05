from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import os
from datetime import datetime
from dotenv import load_dotenv

from db import get_db
from models import Message
from schemas import ReplyRequest, ReplyResponse, MessageData, MessageContent, MessageRole
from cache import message_cache
from queries import MessageQueries

load_dotenv()

app = FastAPI(title="Chat API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Load existing messages from database into cache on startup"""
    db = next(get_db())
    try:
        message_data = MessageQueries.get_recent_messages(db, limit=500)  # Load recent messages
        message_cache.load_from_db(message_data)
        print(f"Loaded {len(message_data)} messages from database into cache")
    except Exception as e:
        print(f"Warning: Could not load messages from database: {e}")
        print("Make sure the database container is running: cd database && ./manage.sh start")
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Chat API is running"}

@app.post("/api/reply", response_model=ReplyResponse)
async def reply_endpoint(request: ReplyRequest, db: Session = Depends(get_db)):
    """
    Handle chat reply requests with the following flow:
    1. Save user message to database and cache
    2. Get chat history from cache for context
    3. Generate assistant response using context
    4. Save assistant response to database and cache
    5. Return assistant response
    """
    try:
        # 1. Save user message to database and cache
        user_message = save_message_and_cache(
            db=db, 
            role=MessageRole.USER, 
            content=request.message
        )
        
        # 2. Get chat history from cache for context
        chat_history = get_chat_history_from_cache(limit=500)
        
        # 3. Generate assistant response using context
        lead_name = "guest"
        if request.lead and isinstance(request.lead, dict):
            lead_name = request.lead.get("name", "guest")
        
        # Generate response (in the future, this would use chat_history for context)
        assistant_content = f"Thanks {lead_name} — ref={uuid.uuid4()}"
        
        # 4. Save assistant response to database and cache
        assistant_message = save_message_and_cache(
            db=db,
            role=MessageRole.ASSISTANT,
            content=assistant_content,
            parent_id=user_message.id
        )
        
        # 5. Return the response
        response = ReplyResponse(
            message=MessageData(
                id=str(assistant_message.id),  # Convert UUID to string
                message=MessageContent(**assistant_message.message),
                created_date=assistant_message.created_date.isoformat()
            )
        )
        
        return response
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/messages")
async def get_messages(limit: int = 100, include_hidden: bool = False):
    """Get message history from cache, filtered by visibility"""
    messages = message_cache.get_message_history(limit=limit, visible_only=not include_hidden)
    return {
        "messages": messages,
        "count": len(messages)
    }

@app.post("/api/test-hidden")
async def test_hidden_message(db: Session = Depends(get_db)):
    """Test endpoint to create a hidden message for debugging"""
    hidden_message = save_message_and_cache(
        db=db,
        role=MessageRole.ASSISTANT,
        content="[INTERNAL] Tool call executed: search_database(query='user_preferences')",
        visible_to_user=False
    )
    
    return {"message": "Hidden message created", "id": str(hidden_message.id)}

# =============================================================================
# Helper Functions
# =============================================================================

def save_message_and_cache(db: Session, role: MessageRole, content: str, parent_id=None, visible_to_user: bool = True) -> Message:
    """
    Save a message to database and add to cache.
    Returns the saved message object.
    """
    # Create JSONB data for storage
    message_jsonb = {
        "role": role.value,
        "content": content,
    }
    
    message = Message(
        message=message_jsonb,
        role=role.value,
        parent_id=parent_id,
        visible_to_user=visible_to_user
    )
    db.add(message)
    db.commit()
    
    # Add to cache after successful database save
    cache_data = message.to_dict()
    message_cache.add_message(cache_data)
    
    return message

def get_chat_history_from_cache(limit: int = 500, include_hidden: bool = True) -> list:
    """Get chat history from cache for AI context (includes hidden messages by default)"""
    return message_cache.get_message_history(limit=limit, visible_only=not include_hidden)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
