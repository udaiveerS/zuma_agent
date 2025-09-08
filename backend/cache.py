from typing import List, Dict, Optional, Any

class UserMessageCache:
    """Cache for storing messages organized by user email"""
    
    def __init__(self):
        # Structure: {email: {"messages": [...], "loaded": bool}}
        self._user_caches: Dict[str, Dict[str, Any]] = {}
    
    def _get_user_cache(self, email: str) -> Dict[str, Any]:
        """Get or create cache for a specific user"""
        if email not in self._user_caches:
            self._user_caches[email] = {
                "messages": [],
                "loaded": False
            }
        return self._user_caches[email]
    
    def add_message(self, email: str, message_data: Dict[str, Any]):
        """Add a message to a user's cache"""
        user_cache = self._get_user_cache(email)
        user_cache["messages"].append(message_data)
    
    def add_messages(self, email: str, messages: List[Dict[str, Any]]):
        """Add multiple messages to a user's cache"""
        for message in messages:
            self.add_message(email, message)
    
    def get_message_history(self, email: str, limit: int = 100, visible_only: bool = True) -> List[Dict[str, Any]]:
        """Get recent message history for a user, optionally filtered by visibility"""
        user_cache = self._get_user_cache(email)
        messages = user_cache["messages"]
        
        if visible_only:
            messages = [msg for msg in messages if msg.get('visible_to_user', True)]
        
        return messages[-limit:] if len(messages) > limit else messages
    
    def load_from_db(self, email: str, messages: List[Dict[str, Any]]):
        """Load messages from database into a user's cache"""
        user_cache = self._get_user_cache(email)
        user_cache["messages"].clear()
        user_cache["messages"].extend(messages)
        user_cache["loaded"] = True
    
    def is_loaded(self, email: str) -> bool:
        """Check if a user's cache has been loaded from DB"""
        user_cache = self._get_user_cache(email)
        return user_cache["loaded"]
    
    def clear(self, email: str):
        """Clear all cached messages for a user"""
        if email in self._user_caches:
            self._user_caches[email]["messages"].clear()
            self._user_caches[email]["loaded"] = False
    
    def clear_all(self):
        """Clear all user caches"""
        self._user_caches.clear()
    
    def size(self, email: str) -> int:
        """Get total number of cached messages for a user"""
        user_cache = self._get_user_cache(email)
        return len(user_cache["messages"])
    
    def get_cached_users(self) -> List[str]:
        """Get list of emails that have cached data"""
        return list(self._user_caches.keys())

# Global cache instance
message_cache = UserMessageCache()