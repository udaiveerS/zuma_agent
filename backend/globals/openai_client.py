"""
Global OpenAI Client

Provides a singleton OpenAI client instance for the entire application.
Uses lazy initialization pattern similar to database connections.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global OpenAI client instance
openai_client = None

def get_openai_client() -> OpenAI:
    """
    Get the global OpenAI client instance.
    Creates the client on first call, returns cached instance on subsequent calls.
    
    Returns:
        OpenAI: Configured OpenAI client instance
        
    Raises:
        ValueError: If OPENAI_API_KEY is not found in environment
    """
    global openai_client
    
    if openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        openai_client = OpenAI(api_key=api_key)
    
    return openai_client
