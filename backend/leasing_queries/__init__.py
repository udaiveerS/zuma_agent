"""
Queries Module

Modular database queries for leasing operations.
Each query type is separated into its own file for better maintainability.
Returns raw JSON data for LLM processing.
"""

from .pet_policy import get_pet_policy
from .pricing import get_pricing

__all__ = [
    'get_pet_policy',
    'get_pricing',
]
