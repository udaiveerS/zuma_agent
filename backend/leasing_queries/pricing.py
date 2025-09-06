"""
Pricing Database Queries

Simple unit pricing lookup with validation.
Returns raw JSON data for LLM processing.
"""

from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import text


def get_pricing(db: Session, community_id: str, unit_id: str, move_in_date: str = None) -> Optional[dict]:
    """
    Get pricing information for a specific unit in a community.
    Returns raw JSON data if the unit exists in that community.
    
    Args:
        db: Database session
        community_id: Community identifier string (e.g., 'sunset-ridge')
        unit_id: Unit code string (e.g., 'B201', 'A102')
        move_in_date: Optional move-in date for specials calculation
    
    Returns:
        Dict with complete unit pricing data or None if unit not found in community
    """
    
    query = text("""
        -- Get unit pricing data with community validation
        SELECT 
            u.unit_id,
            u.community_id,
            u.unit_code,
            u.bedrooms,
            u.bathrooms,
            u.rent,
            u.specials,
            u.availability_status,
            u.available_at,
            c.name as community_name
            
        FROM units u
        INNER JOIN communities c ON u.community_id = c.community_id
        WHERE u.unit_code = :unit_code
            AND u.community_id = :community_id
        LIMIT 1;
    """)
    
    try:
        result = db.execute(query, {
            'unit_code': unit_id,  # unit_id parameter is actually the unit_code
            'community_id': community_id
        }).fetchone()
        
        if not result:
            return None
            
        return {
            'unit_id': str(result.unit_id),
            'community_id': str(result.community_id),
            'unit_code': result.unit_code,
            'bedrooms': result.bedrooms,
            'bathrooms': float(result.bathrooms),
            'rent': float(result.rent),
            'specials': result.specials,
            'availability_status': result.availability_status,
            'available_at': result.available_at.isoformat() if result.available_at else None,
            'community_name': result.community_name,
        }
        
    except Exception as e:
        print(f"Error getting pricing: {e}")
        return None


