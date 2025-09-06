# prompts/friendly_chat_prompt.py
from ..base_prompt import SimplePrompt
from typing import Optional, Dict

class FriendlyChatPrompt(SimplePrompt):
    """Prompt for friendly conversation that doesn't require tools."""
    
    def __init__(self, user_query: str, context: Optional[Dict] = None):
        # Enhanced prompt for friendly conversation
        enhanced_prompt = f"""
User says: {user_query}

Please respond in a friendly, conversational manner. Keep the conversation going 
by being engaging, asking follow-up questions when appropriate, and showing 
genuine interest in what the user is sharing. No tools are needed for this conversation.
"""
        super().__init__(enhanced_prompt.strip(), context=context)
