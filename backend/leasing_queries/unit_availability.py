"""
Unit Availability Database Queries

Handles unit availability lookups based on community, bedrooms, and move-in date.
Designed for AI agent tool integration with clean JSON responses.
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import text


def get_available_units(
    db: Session, 
    community_id: str, 
    bedrooms: int, 
    move_in_date: str = None
) -> List[dict]:
    """
    Get available units for a community matching bedroom count and move-in date.
    
    Args:
        db: Database session
        community_id: Community identifier string (e.g., 'sunset-ridge')
        bedrooms: Number of bedrooms required
        move_in_date: Desired move-in date (YYYY-MM-DD format), optional
    
    Returns:
        List of available units with complete details, or None if error
        
    Business Logic:
        - 'available': Units ready immediately
        - 'notice': Units where tenant gave notice, available at 'available_at' date
        - Only show 'notice' units if available_at <= move_in_date
        - Exclude 'occupied' and 'offline' units
    """
    
    # Base query for available units
    query_conditions = [
        "u.community_id = :community_id",
        "u.bedrooms = :bedrooms",
        "(u.availability_status = 'available' OR u.availability_status = 'notice')"
    ]
    
    query_params = {
        'community_id': community_id,
        'bedrooms': bedrooms
    }
    
    # Add move-in date filter for 'notice' units if provided
    if move_in_date:
        query_conditions.append("""
            (u.availability_status = 'available' 
             OR (u.availability_status = 'notice' AND u.available_at <= :move_in_date))
        """)
        query_params['move_in_date'] = move_in_date
    else:
        # If no move-in date provided, only show currently available units
        query_conditions.append("u.availability_status = 'available'")
    
    query = text(f"""
        -- Get available units with community validation
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
        WHERE {' AND '.join(query_conditions)}
        ORDER BY u.rent ASC, u.unit_code ASC;
    """)
    
    try:
        results = db.execute(query, query_params).fetchall()
        
        if not results:
            return []
            
        units = []
        for result in results:
            units.append({
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
            })
            
        return units
        
    except Exception as e:
        print(f"Error getting available units: {e}")
        return None
