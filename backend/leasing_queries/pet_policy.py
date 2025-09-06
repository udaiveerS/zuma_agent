"""
Pet Policy Database Queries

Handles pet policy lookups from community_policies table.
Designed for AI agent tool integration with clean JSON responses.
"""

from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import text


def get_pet_policy(db: Session, community_id: str) -> Optional[dict]:
    """
    Get the complete pet policy JSON for a community.
    Returns the raw JSON blob for LLM to parse and interpret.
    
    Args:
        db: Database session
        community_id: Community identifier string (e.g., 'sunset-ridge')
    
    Returns:
        Dict containing the complete pet policy rules or None if not found
    
    SQL Logic:
        1. Query community_policies table directly with string identifier
        2. Return the complete rules JSON blob
    
    Example JSON structure returned:
        {
            "cat": {"allowed": true, "fee": 50, "notes": "Indoor only"},
            "dog": {"allowed": false},
            "default": {"allowed": false, "notes": "Contact office for other pets"}
        }
    """
    
    # Direct query using string identifier (no UUID lookup needed after migration)
    policy_query = text("""
        -- Pet Policy Query - Return complete JSON
        SELECT 
            cp.community_id,
            cp.rules as pet_policy
        FROM community_policies cp
        WHERE cp.community_id = :community_id
            AND cp.policy_type = 'pet'
        LIMIT 1;
    """)
    
    try:
        result = db.execute(policy_query, {'community_id': community_id}).fetchone()
        
        if not result:
            return None
            
        return {
            'community_id': community_id,
            'pet_policy': result.pet_policy  # This is the raw JSON blob
        }
        
    except Exception as e:
        # Log error in production
        print(f"Error getting pet policy: {e}")
        return None


