# prompts/get_property_info.py
from ..base_prompt import ToolPrompt
from typing import Optional, Dict
import logging

# Set up logger for this module
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class GetPropertyInfoPrompt(ToolPrompt):
    """Prompt for handling property and unit availability queries."""
    
    def __init__(self, user_query: str, context: Optional[Dict] = None):
        self.original_query = user_query
        
        # Extract context information
        community_id = context.get('community_id', '') if context else ''
        move_in_date = context.get('move_in_date', '') if context else ''
        bedrooms = context.get('bedrooms', '') if context else ''
        user_name = context.get('name', 'there') if context else 'there'
        
        # Build property info prompt
        property_info_prompt = f"""
You are a helpful leasing assistant for {community_id or 'this community'}. 

User: "{user_query}"

Context: Community: {community_id}, Move-in: {move_in_date or 'flexible'}, Bedrooms: {bedrooms or 'any'}, Name: {user_name}

Use these tools as needed:
- check_availability: For "do you have units available?" questions
- get_pricing: For "how much is rent?" questions about specific units  
- check_pet_policy: For pet questions (cat, dog, bird, fish, rabbit, hamster)

Keep responses brief and conversational. No bold text. Always include unit codes for reference.
"""
        
        super().__init__(property_info_prompt, context=context)
        
    def execute(self, agent, msgs):
        """Execute the property info prompt with enhanced logging."""
        logger.info(f"🏠 PROPERTY_INFO: Processing query: '{self.original_query}'")
        logger.info(f"🏠 PROPERTY_INFO: Context - Community: {self.context.get('community_id', 'N/A')}, "
                   f"Bedrooms: {self.context.get('bedrooms', 'N/A')}, "
                   f"Move-in: {self.context.get('move_in_date', 'N/A')}")
        
        result = super().execute(agent, msgs)
        
        logger.info(f"🏠 PROPERTY_INFO: Response generated: {result[:100]}...")
        return result
