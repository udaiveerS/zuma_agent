"""
Global Instances Module

Centralized location for all global application instances.
Keeps the main backend directory clean and organized.

Different patterns for different needs:
- Database: Per-request sessions (eager initialization)
- OpenAI Client: Singleton (lazy initialization) 
- Agent: Singleton (lazy initialization)
"""

from .database import get_db
from .openai_client import get_openai_client
from .agent_instance import get_agent

__all__ = [
    'get_db',
    'get_openai_client',
    'get_agent',
]
