from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional


from datetime import datetime
from dotenv import load_dotenv

from globals import get_db
from models import Message
from schemas import ReplyRequest, ReplyResponse, MessageData, MessageContent, MessageRole, ActionType, BookingResponse
from cache import message_cache
from queries import MessageQueries

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    """Load existing messages from database into cache on startup"""
    db = next(get_db())
    try:
        message_data = MessageQueries.get_recent_messages(db, limit=50)  # Load recent messages (optimized)
        message_cache.load_from_db(message_data)
        print(f"Loaded {len(message_data)} messages from database into cache")
    except Exception as e:
        print(f"Warning: Could not load messages from database: {e}")
        print("Make sure the database container is running: cd database && ./manage.sh start")
    finally:
        db.close()
    
    yield  # Application runs here
    
    # Shutdown (optional cleanup)
    print("Application shutting down...")

app = FastAPI(title="Chat API", version="1.0.0", lifespan=lifespan)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Chat API is running"}

@app.post("/api/reply", response_model=ReplyResponse)
async def reply_endpoint(request: ReplyRequest, db: Session = Depends(get_db)):
    """
    Handle chat reply requests with the following flow:
    1. Save user message to database and cache
    2. Get chat history from cache for context
    3. Route through security classification (RouterPrompt)
    4. Generate structured BookingResponse using tools if needed
    5. Save assistant response to database and cache
    6. Return structured response with action classification
    """
    try:
        # 1. Save user message to database and cache
        user_message = save_message_and_cache(
            db=db, 
            role=MessageRole.USER, 
            content=request.message
        )
        
        # 2. Get chat history from cache for context
        recent_messages = message_cache.get_message_history(limit=30, visible_only=False)  # Reduced for performance
                

        # Generate response using the agent
        from globals import get_agent
        agent = get_agent()
        
        # Convert to format expected by agent (list of dicts with role/content)
        conversation_history = []
        for msg in recent_messages:  # Include all messages including current user message
            conversation_history.append({
                "role": msg.get("role", "user"),
                "content": msg.get("message", {}).get("content", "")
            })
        
        # Build context from request
        context = {
            "community_id": request.community_id,
            "move_in_date": request.preferences.get("move_in") if request.preferences else None,
            "bedrooms": request.preferences.get("bedrooms") if request.preferences else None,
            "name": request.lead.get("name") if request.lead else None,
            "email": request.lead.get("email") if request.lead else None,
        }
        
        # Get agent response using RouterPrompt (like in booking_agent/main.py)
        from booking_agent.prompts.router_prompt import RouterPrompt
        router = RouterPrompt(request.message, context=context)
        booking_response = agent.run(router, conversation_history, request_id=str(user_message.id))

        # Extract content for database storage
        assistant_content = booking_response.reply

        # 4. Generate UUID first, then save assistant response to database and cache
        import uuid
        response_uuid = str(uuid.uuid4())
        
        assistant_message = save_message_and_cache_with_id(
            db=db,
            message_id=response_uuid,
            role=MessageRole.ASSISTANT,
            content=assistant_content,
            parent_id=user_message.id
        )
        
        # 5. Return the response using BookingResponse data
        response = ReplyResponse(
            id=response_uuid,  # Use the same UUID we saved to DB
            reply=booking_response.reply,
            created_date=assistant_message.created_date.isoformat(),  # Use the actual DB timestamp
            action=booking_response.action,
            propose_time=booking_response.propose_time
        )
        
        return response
        
    except Exception as e:
        print(f"❌ ERROR in reply_endpoint: {str(e)}")
        import traceback
        print(f"📍 Full traceback:\n{traceback.format_exc()}")
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

def save_message_and_cache_with_id(db: Session, message_id: str, role: MessageRole, content: str, parent_id=None, visible_to_user: bool = True) -> Message:
    """
    Save a message to database and add to cache with a specific UUID.
    Returns the saved message object.
    """
    import uuid
    
    # Create JSONB data for storage
    message_jsonb = {
        "role": role.value,
        "content": content,
    }
    
    message = Message(
        id=uuid.UUID(message_id),  # Use the provided UUID
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
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, workers=1)
