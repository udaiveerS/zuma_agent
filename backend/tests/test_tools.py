#!/usr/bin/env python3
"""
Unit Tests for Zuma Agent Tools

Tests the individual tool functions:
1. check_availability - success scenario
2. check_availability - no availability scenario  
3. get_pricing - pricing lookup
4. check_pet_policy - pet policy lookup

Run with: python -m pytest tests/test_tools.py -v
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import the tool functions directly to avoid circular imports
def check_availability(community_id: str, bedrooms: int, move_in_date: str = None):
    """Mock implementation for testing - imports done inside function"""
    from booking_agent.tools import check_availability as _check_availability
    return _check_availability(community_id, bedrooms, move_in_date)

def get_pricing(community_id: str, unit_id: str, move_in_date: str = None):
    """Mock implementation for testing - imports done inside function"""
    from booking_agent.tools import get_pricing as _get_pricing
    return _get_pricing(community_id, unit_id, move_in_date)

def check_pet_policy(community_id: str, pet_type: str):
    """Mock implementation for testing - imports done inside function"""  
    from booking_agent.tools import check_pet_policy as _check_pet_policy
    return _check_pet_policy(community_id, pet_type)


class TestCheckAvailability:
    """Test check_availability tool"""
    
    @patch('booking_agent.tools.get_db')
    @patch('booking_agent.tools.db_get_available_units')
    def test_availability_success(self, mock_db_get_units, mock_get_db):
        """Test successful availability check with units found"""
        # Mock database connection
        mock_db = Mock()
        mock_get_db.return_value = iter([mock_db])
        
        # Mock successful response with units
        mock_db_get_units.return_value = [
            {
                "unit_code": "B201",
                "bedrooms": 2,
                "bathrooms": 2,
                "availability_status": "available",
                "available_at": "2025-01-01"
            },
            {
                "unit_code": "B202", 
                "bedrooms": 2,
                "bathrooms": 2,
                "availability_status": "available",
                "available_at": "2025-01-15"
            }
        ]
        
        # Call the function
        result = check_availability("sunset-ridge", 2)
        
        # Assertions
        assert result["success"] is True
        assert result["count"] == 2
        assert len(result["units"]) == 2
        assert result["units"][0]["unit_code"] == "B201"
        assert result["units"][1]["unit_code"] == "B202"
        
        # Verify database interactions
        mock_db_get_units.assert_called_once_with(
            db=mock_db,
            community_id="sunset-ridge",
            bedrooms=2,
            move_in_date=None
        )
        mock_db.close.assert_called_once()
    
    @patch('booking_agent.tools.get_db')
    @patch('booking_agent.tools.db_get_available_units')
    def test_no_availability_scenario(self, mock_db_get_units, mock_get_db):
        """Test availability check with no units found"""
        # Mock database connection
        mock_db = Mock()
        mock_get_db.return_value = iter([mock_db])
        
        # Mock empty response (no units available)
        mock_db_get_units.return_value = []
        
        # Call the function
        result = check_availability("sunset-ridge", 5)  # 5-bedroom units don't exist
        
        # Assertions
        assert result["success"] is True
        assert result["count"] == 0
        assert len(result["units"]) == 0
        
        # Verify database interactions
        mock_db_get_units.assert_called_once_with(
            db=mock_db,
            community_id="sunset-ridge", 
            bedrooms=5,
            move_in_date=None
        )
        mock_db.close.assert_called_once()
    
    @patch('booking_agent.tools.get_db')
    @patch('booking_agent.tools.db_get_available_units')
    def test_availability_database_error(self, mock_db_get_units, mock_get_db):
        """Test availability check with database error"""
        # Mock database connection
        mock_db = Mock()
        mock_get_db.return_value = iter([mock_db])
        
        # Mock database returning None (error case)
        mock_db_get_units.return_value = None
        
        # Call the function
        result = check_availability("sunset-ridge", 2)
        
        # Assertions
        assert result["success"] is False
        assert result["error"] == "Database error occurred"
        assert result["units"] == []
        
        # Verify database connection was closed
        mock_db.close.assert_called_once()


class TestGetPricing:
    """Test get_pricing tool"""
    
    @patch('booking_agent.tools.get_db')
    @patch('booking_agent.tools.db_get_pricing')
    def test_pricing_success(self, mock_db_get_pricing, mock_get_db):
        """Test successful pricing lookup"""
        # Mock database connection
        mock_db = Mock()
        mock_get_db.return_value = iter([mock_db])
        
        # Mock pricing response
        mock_db_get_pricing.return_value = {
            "unit_code": "B201",
            "rent": 2500,
            "specials": "First month free",
            "bedrooms": 2,
            "bathrooms": 2,
            "availability_status": "available",
            "available_at": "2025-01-01",
            "community_name": "Sunset Ridge"
        }
        
        # Call the function
        result = get_pricing("sunset-ridge", "B201")
        
        # Assertions
        assert result["success"] is True
        assert result["unit_code"] == "B201"
        assert result["rent"] == 2500
        assert result["specials"] == "First month free"
        assert result["bedrooms"] == 2
        assert result["community_name"] == "Sunset Ridge"
        
        # Verify database interactions
        mock_db_get_pricing.assert_called_once_with(
            db=mock_db,
            community_id="sunset-ridge",
            unit_id="B201",
            move_in_date=None
        )
        mock_db.close.assert_called_once()
    
    @patch('booking_agent.tools.get_db')
    @patch('booking_agent.tools.db_get_pricing')
    def test_pricing_unit_not_found(self, mock_db_get_pricing, mock_get_db):
        """Test pricing lookup for non-existent unit"""
        # Mock database connection
        mock_db = Mock()
        mock_get_db.return_value = iter([mock_db])
        
        # Mock unit not found
        mock_db_get_pricing.return_value = None
        
        # Call the function
        result = get_pricing("sunset-ridge", "INVALID")
        
        # Assertions
        assert result["success"] is False
        assert result["error"] == "Unit 'INVALID' not found in community 'sunset-ridge'"
        
        # Verify database connection was closed
        mock_db.close.assert_called_once()


class TestCheckPetPolicy:
    """Test check_pet_policy tool"""
    
    @patch('booking_agent.tools.get_db')
    @patch('booking_agent.tools.db_get_pet_policy')
    def test_pet_policy_success(self, mock_db_get_pet_policy, mock_get_db):
        """Test successful pet policy lookup"""
        # Mock database connection
        mock_db = Mock()
        mock_get_db.return_value = iter([mock_db])
        
        # Mock pet policy response
        mock_db_get_pet_policy.return_value = {
            "pet_policy": {
                "cats": {
                    "allowed": True,
                    "fee": 50,
                    "deposit": 200,
                    "notes": "Indoor cats only",
                    "restrictions": "Maximum 2 cats"
                },
                "dogs": {
                    "allowed": True,
                    "fee": 75,
                    "deposit": 300,
                    "notes": "All breeds welcome",
                    "restrictions": "Maximum 2 dogs, weight limit 80lbs"
                }
            }
        }
        
        # Call the function
        result = check_pet_policy("sunset-ridge", "cats")
        
        # Assertions
        assert result["success"] is True
        assert result["pet_type"] == "cats"
        assert result["allowed"] is True
        assert result["fee"] == 50
        assert result["deposit"] == 200
        assert result["notes"] == "Indoor cats only"
        assert result["restrictions"] == "Maximum 2 cats"
        
        # Verify database interactions
        mock_db_get_pet_policy.assert_called_once_with(
            db=mock_db,
            community_id="sunset-ridge"
        )
        mock_db.close.assert_called_once()
    
    @patch('booking_agent.tools.get_db')
    @patch('booking_agent.tools.db_get_pet_policy')
    def test_pet_policy_default_fallback(self, mock_db_get_pet_policy, mock_get_db):
        """Test pet policy with default fallback for unknown pet type"""
        # Mock database connection
        mock_db = Mock()
        mock_get_db.return_value = iter([mock_db])
        
        # Mock pet policy response with default policy
        mock_db_get_pet_policy.return_value = {
            "pet_policy": {
                "cats": {
                    "allowed": True,
                    "fee": 50,
                    "deposit": 200
                },
                "default": {
                    "allowed": False,
                    "notes": "Please contact office for exotic pets"
                }
            }
        }
        
        # Call the function with unknown pet type
        result = check_pet_policy("sunset-ridge", "ferret")
        
        # Assertions
        assert result["success"] is True
        assert result["pet_type"] == "ferret"
        assert result["allowed"] is False
        assert result["notes"] == "Please contact office for exotic pets"
        
        # Verify database connection was closed
        mock_db.close.assert_called_once()
    
    @patch('booking_agent.tools.get_db')
    @patch('booking_agent.tools.db_get_pet_policy')
    def test_pet_policy_not_found(self, mock_db_get_pet_policy, mock_get_db):
        """Test pet policy lookup when no policy exists"""
        # Mock database connection
        mock_db = Mock()
        mock_get_db.return_value = iter([mock_db])
        
        # Mock no pet policy found
        mock_db_get_pet_policy.return_value = None
        
        # Call the function
        result = check_pet_policy("invalid-community", "cats")
        
        # Assertions
        assert result["success"] is False
        assert result["error"] == "No pet policy found for this community"
        
        # Verify database connection was closed
        mock_db.close.assert_called_once()


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])
