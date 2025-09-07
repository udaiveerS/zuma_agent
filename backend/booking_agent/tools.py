# booking_agent/tools.py
"""
Simple tools for the booking agent.
All tools in one file - clean and simple.
"""

from typing import Dict, Any
from globals.database import get_db
from leasing_queries.unit_availability import get_available_units as db_get_available_units
from leasing_queries.pet_policy import get_pet_policy as db_get_pet_policy
from leasing_queries.pricing import get_pricing as db_get_pricing


def check_availability(community_id: str, bedrooms: int, move_in_date: str = None) -> Dict[str, Any]:
    """Check availability for a community matching bedroom count and move-in date."""
    try:
        db = next(get_db())
        try:
            units = db_get_available_units(
                db=db, 
                community_id=community_id, 
                bedrooms=bedrooms, 
                move_in_date=move_in_date
            )
            
            if units is None:
                return {
                    "success": False,
                    "error": "Database error occurred",
                    "units": []
                }
            
            # Return only unit codes and availability status - NO PRICING
            availability_units = []
            for unit in units:
                availability_units.append({
                    "unit_code": unit.get("unit_code"),
                    "bedrooms": unit.get("bedrooms"),
                    "bathrooms": unit.get("bathrooms"),
                    "availability_status": unit.get("availability_status"),
                    "available_at": unit.get("available_at")
                })
            
            return {
                "success": True,
                "units": availability_units,
                "count": len(units)
            }
        finally:
            db.close()  # Always close, even if exception occurs
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error retrieving units: {str(e)}",
            "units": []
        }


def get_pricing(community_id: str, unit_id: str, move_in_date: str = None) -> Dict[str, Any]:
    """Get pricing information for a specific unit."""
    try:
        db = next(get_db())
        try:
            pricing = db_get_pricing(
                db=db, 
                community_id=community_id, 
                unit_id=unit_id, 
                move_in_date=move_in_date
            )
            
            if pricing is None:
                return {
                    "success": False,
                    "error": f"Unit '{unit_id}' not found in community '{community_id}'"
                }
            
            return {
                "success": True,
                "unit_code": pricing.get('unit_code'),
                "rent": pricing.get('rent'),
                "specials": pricing.get('specials'),
                "bedrooms": pricing.get('bedrooms'),
                "bathrooms": pricing.get('bathrooms'),
                "availability_status": pricing.get('availability_status'),
                "available_at": pricing.get('available_at'),
                "community_name": pricing.get('community_name')
            }
        finally:
            db.close()  # Always close, even if exception occurs
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error retrieving pricing: {str(e)}"
        }



def check_pet_policy(community_id: str, pet_type: str) -> Dict[str, Any]:
    """Check pet policy for a specific pet type in a community."""
    try:
        db = next(get_db())
        try:
            policy = db_get_pet_policy(db=db, community_id=community_id)
            
            if policy is None:
                return {
                    "success": False,
                    "error": "No pet policy found for this community"
                }
            
            # Get pet policy rules and look for the pet type
            pet_policy_rules = policy.get('pet_policy', {})
            pet_info = pet_policy_rules.get(pet_type.lower())
            
            if pet_info:
                return {
                    "success": True,
                    "pet_type": pet_type,
                    "allowed": pet_info.get('allowed', False),
                    "fee": pet_info.get('fee'),
                    "deposit": pet_info.get('deposit'),
                    "notes": pet_info.get('notes'),
                    "restrictions": pet_info.get('restrictions')
                }
            else:
                # Check for default policy
                default_policy = pet_policy_rules.get('default', {})
                return {
                    "success": True,
                    "pet_type": pet_type,
                    "allowed": default_policy.get('allowed', False),
                    "notes": default_policy.get('notes', f"No specific policy for {pet_type}. Contact office for details.")
                }
        finally:
            db.close()  # Always close, even if exception occurs
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error checking pet policy: {str(e)}"
        }


# Tool specifications for OpenAI function calling
TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Check availability for a community matching bedroom count and optional move-in date. Returns available units with unit codes for reference. Use this for availability questions only.",
            "parameters": {
                "type": "object",
                "properties": {
                    "community_id": {
                        "type": "string",
                        "description": "Community identifier (e.g., 'sunset-ridge', 'downtown-lofts')"
                    },
                    "bedrooms": {
                        "type": "integer",
                        "description": "Number of bedrooms required"
                    },
                    "move_in_date": {
                        "type": ["string", "null"],
                        "description": "Optional desired move-in date in YYYY-MM-DD format. If provided, only shows units available by this date."
                    }
                },
                "required": ["community_id", "bedrooms", "move_in_date"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pricing",
            "description": "Get pricing information for a specific unit. Use this when users ask about rent, cost, pricing, or specials for a specific unit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "community_id": {
                        "type": "string",
                        "description": "Community identifier (e.g., 'sunset-ridge', 'downtown-lofts')"
                    },
                    "unit_id": {
                        "type": "string",
                        "description": "Unit code (e.g., 'B201', 'A102')"
                    },
                    "move_in_date": {
                        "type": ["string", "null"],
                        "description": "Optional move-in date in YYYY-MM-DD format for specials calculation"
                    }
                },
                "required": ["community_id", "unit_id", "move_in_date"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_pet_policy",
            "description": "Check if a specific pet type is allowed. Valid pet types: cat, dog, bird, fish, rabbit, hamster. Use lowercase.",
            "parameters": {
                "type": "object",
                "properties": {
                    "community_id": {
                        "type": "string",
                        "description": "Community identifier (e.g., 'sunset-ridge', 'downtown-lofts')"
                    },
                    "pet_type": {
                        "type": "string",
                        "description": "Pet type in lowercase: cat, dog, bird, fish, rabbit, hamster"
                    }
                },
                "required": ["community_id", "pet_type"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
]

# Tool implementations mapping
TOOL_IMPLS = {
    "check_availability": check_availability,
    "get_pricing": get_pricing,
    "check_pet_policy": check_pet_policy,
}