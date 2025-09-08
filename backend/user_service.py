"""
User service for managing user storage and preferences
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

def get_or_create_user(
    db: Session, 
    email: str, 
    name: str, 
    preferences: Optional[Dict[str, Any]] = None
) -> User:
    """
    Get existing user or create new one with upsert pattern.
    
    Args:
        db: Database session
        email: User email (unique identifier, required)
        name: User display name (required)
        preferences: User preferences dictionary
    
    Returns:
        User object (existing or newly created)
    
    Raises:
        ValueError: If email or name is None or empty
    """
    try:
        # Validate required fields
        if not email or not email.strip():
            raise ValueError("Email is required for user creation")
        
        if not name or not name.strip():
            raise ValueError("Name is required for user creation")
        
        email = email.strip()
        name = name.strip()
        
        # Try to get existing user
        user = db.query(User).filter(User.email == email).first()
        
        if user:
            # Update existing user if data has changed
            updated = False
            
            if name and user.name != name:
                user.name = name
                updated = True
                
            if preferences:
                # Merge preferences (new preferences override existing ones)
                current_prefs = user.preferences or {}
                merged_prefs = {**current_prefs, **preferences}
                
                if merged_prefs != current_prefs:
                    user.preferences = merged_prefs
                    updated = True
            
            if updated:
                db.commit()
                logger.info(f"Updated existing user: {email}")
            
            return user
        
        else:
            # Create new user
            new_user = User(
                email=email,
                name=name,
                preferences=preferences or {}
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)  # Get the generated user_id
            
            logger.info(f"Created new user: {email} with ID: {new_user.user_id}")
            return new_user
            
    except IntegrityError as e:
        # Handle race condition where another request created the user
        db.rollback()
        logger.warning(f"Race condition creating user {email}, retrying...")
        
        # Try to get the user that was created by another request
        user = db.query(User).filter(User.email == email).first()
        if user:
            return user
        else:
            # If still not found, re-raise the error
            raise e
    except Exception as e:
        db.rollback()
        logger.error(f"Error in get_or_create_user for {email}: {str(e)}")
        raise e

def update_user_preferences(
    db: Session, 
    user_id: str, 
    preferences: Dict[str, Any]
) -> Optional[User]:
    """
    Update user preferences by user_id.
    
    Args:
        db: Database session
        user_id: User UUID as string
        preferences: New preferences to merge
    
    Returns:
        Updated User object or None if not found
    """
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        
        if user:
            user.update_preferences(preferences)
            db.commit()
            logger.info(f"Updated preferences for user {user_id}")
            return user
        else:
            logger.warning(f"User not found for update: {user_id}")
            return None
            
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating preferences for user {user_id}: {str(e)}")
        raise e

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get user by email address.
    
    Args:
        db: Database session
        email: User email
    
    Returns:
        User object or None if not found
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """
    Get user by user_id.
    
    Args:
        db: Database session
        user_id: User UUID as string
    
    Returns:
        User object or None if not found
    """
    return db.query(User).filter(User.user_id == user_id).first()
