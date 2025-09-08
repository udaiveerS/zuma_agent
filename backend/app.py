from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional


from datetime import datetime
from dotenv import load_dotenv

from globals import get_db
from models import Message, User
from schemas import ReplyRequest, ReplyResponse, MessageData, MessageContent, MessageRole, ActionType, BookingResponse
from cache import message_cache
from queries import MessageQueries
from user_service import get_or_create_user

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    """Load existing messages from database into cache on startup"""
    db = next(get_db())
    try:
        message_data = MessageQueries.get_recent_messages(db, limit=50)  # Load recent messages (optimized)
        
        for email, messages in message_data.items():
            message_cache.load_from_db(email, messages)
            total_loaded += len(messages)
            print(f"Loaded {len(messages)} messages for user {email}")
        
        print(f"Total loaded: {total_loaded} messages from database into cache")
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
    6. Return structured response with action classificationt
    """
    try:
        # 1. Handle user - get or create user with preferences
        # Pydantic has already validated that lead.email and lead.name exist and are valid
        user_email = request.lead.email
        user_name = request.lead.name
        user_preferences = request.preferences or {}
        
        # Get or create user in database
        user = get_or_create_user(
            db=db,
            email=user_email,
            name=user_name,
            preferences=user_preferences
        )
        
        # Use the actual email from the user object (in case it was generated)
        user_email = user.email
        
        # 2. Save user message to database and cache with user_id
        user_message = save_message_and_cache_with_user(
            db=db, 
            role=MessageRole.USER, 
            content=request.message,
            user_id=user.user_id,
            user_email=user_email
        )
        
        # 3. Get chat history from cache for this user
        recent_messages = message_cache.get_message_history(user_email, limit=30, visible_only=False)
                

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
        
        # Build context from user preferences and request
        context = {
            "community_id": request.community_id,
            "move_in_date": user.preferences.get("move_in") or (request.preferences.get("move_in") if request.preferences else None),
            "bedrooms": user.preferences.get("bedrooms") or (request.preferences.get("bedrooms") if request.preferences else None),
            "name": user.name,
            "email": user.email,
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
        
        assistant_message = save_message_and_cache_with_user(
            db=db,
            role=MessageRole.ASSISTANT,
            content=assistant_content,
            user_id=user.user_id,
            user_email=user_email,
            parent_id=user_message.id,
            message_id=response_uuid
        )
        
        # 5. Return the response using BookingResponse data
        response = ReplyResponse(
            id=response_uuid,  # Use the same UUID we saved to DB
            reply=booking_response.reply,
            created_date=assistant_message.created_date.isoformat(),  # Use the actual DB timestamp
            action=booking_response.action,
            propose_time=booking_response.propose_time,
            parent_id=str(user_message.id)  # Include the parent_id (user message ID)
        )
        
        return response
        
    except Exception as e:
        print(f"❌ ERROR in reply_endpoint: {str(e)}")
        import traceback
        print(f"📍 Full traceback:\n{traceback.format_exc()}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/messages")
async def get_messages(email: str, limit: int = 100, include_hidden: bool = False):
    """Get message history from cache for a specific user, filtered by visibility"""
    messages = message_cache.get_message_history(email, limit=limit, visible_only=not include_hidden)
    
    # Clean up message format for frontend compatibility
    cleaned_messages = []
    for msg in messages:
        cleaned_msg = {
            "id": msg.get("id"),
            "message": msg.get("message", {}),
            "created_date": msg.get("created_date")
        }
        cleaned_messages.append(cleaned_msg)
    
    return {
        "messages": cleaned_messages,
        "count": len(cleaned_messages)
    }


# =============================================================================
# Helper Functions
# =============================================================================


def save_message_and_cache_with_user(db: Session, role: MessageRole, content: str, user_id: str, user_email: str, parent_id=None, visible_to_user: bool = True, message_id: str = None) -> Message:
    """
    Save a message to database and add to user's cache.
    Optionally accepts a specific message_id, otherwise auto-generates one.
    Returns the saved message object.
    """
    import uuid
    
    # Create JSONB data for storage
    message_jsonb = {
        "role": role.value,
        "content": content,
    }
    
    # Create message with optional custom ID
    message_kwargs = {
        "message": message_jsonb,
        "role": role.value,
        "parent_id": parent_id,
        "user_id": user_id,
        "visible_to_user": visible_to_user
    }
    
    if message_id:
        message_kwargs["id"] = uuid.UUID(message_id)
    
    message = Message(**message_kwargs)
    db.add(message)
    db.commit()
    
    # Add to user's cache after successful database save
    cache_data = message.to_dict()
    message_cache.add_message(user_email, cache_data)
    
    return message



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, workers=1)
