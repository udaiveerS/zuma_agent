from typing import List, Dict, Optional, Any

class InProcessCache:
    """Simple in-process cache for storing messages for a single user"""
    
    def __init__(self):
        self._messages: List[Dict[str, Any]] = []
        self._loaded = False
    
    def add_message(self, message_data: Dict[str, Any]):
        """Add a message to the cache"""
        self._messages.append(message_data)
    
    def add_messages(self, messages: List[Dict[str, Any]]):
        """Add multiple messages to the cache"""
        for message in messages:
            self.add_message(message)
    
    def get_message_history(self, limit: int = 100, visible_only: bool = True) -> List[Dict[str, Any]]:
        """Get recent message history, optionally filtered by visibility"""
        messages = self._messages
        
        if visible_only:
            messages = [msg for msg in messages if msg.get('visible_to_user', True)]
        
        return messages[-limit:] if len(messages) > limit else messages
    
    def load_from_db(self, messages: List[Dict[str, Any]]):
        """Load messages from database into cache"""
        self._messages.clear()
        self._messages.extend(messages)
        self._loaded = True
    
    def is_loaded(self) -> bool:
        return self._loaded
    
    def clear(self):
        """Clear all cached messages"""
        self._messages.clear()
        self._loaded = False
    
    def size(self) -> int:
        """Get total number of cached messages"""
        return len(self._messages)

# Global cache instance
message_cache = InProcessCache()