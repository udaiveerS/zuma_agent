# response/agent_response.py
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class AgentResponse:
    """
    Response class for agent interactions.
    Contains both the response text and clean conversation history for frontend.
    """
    
    # The agent's response to the current query
    response: str
    
    # Clean conversation history safe for frontend display
    # Contains only user ↔ assistant messages, no system prompts or tool data
    conversation_history: List[Dict[str, str]]
    
    # Optional metadata
    metadata: Optional[Dict] = None
    
    def __post_init__(self):
        """Validate the response data."""
        if not isinstance(self.response, str):
            raise TypeError("response must be a string")
        
        if not isinstance(self.conversation_history, list):
            raise TypeError("conversation_history must be a list")
        
        # Validate conversation history format
        for msg in self.conversation_history:
            if not isinstance(msg, dict):
                raise TypeError("Each message in conversation_history must be a dict")
            
            if 'role' not in msg or 'content' not in msg:
                raise ValueError("Each message must have 'role' and 'content' keys")
            
            if msg['role'] not in ['user', 'assistant']:
                raise ValueError("Message role must be 'user' or 'assistant'")
    
    @property
    def last_user_message(self) -> Optional[str]:
        """Get the last user message from conversation history."""
        for msg in reversed(self.conversation_history):
            if msg['role'] == 'user':
                return msg['content']
        return None
    
    @property
    def message_count(self) -> int:
        """Get total number of messages in conversation history."""
        return len(self.conversation_history)
    
    @property
    def user_message_count(self) -> int:
        """Get number of user messages in conversation history."""
        return len([msg for msg in self.conversation_history if msg['role'] == 'user'])
    
    @property
    def assistant_message_count(self) -> int:
        """Get number of assistant messages in conversation history."""
        return len([msg for msg in self.conversation_history if msg['role'] == 'assistant'])
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'response': self.response,
            'conversation_history': self.conversation_history,
            'metadata': self.metadata,
            'stats': {
                'total_messages': self.message_count,
                'user_messages': self.user_message_count,
                'assistant_messages': self.assistant_message_count
            }
        }
    
    def get_conversation_for_display(self) -> str:
        """Get formatted conversation string for display."""
        lines = []
        for msg in self.conversation_history:
            role = msg['role'].capitalize()
            content = msg['content']
            lines.append(f"{role}: {content}")
        return "\n".join(lines)
    
    def add_metadata(self, key: str, value) -> None:
        """Add metadata to the response."""
        if self.metadata is None:
            self.metadata = {}
        self.metadata[key] = value
