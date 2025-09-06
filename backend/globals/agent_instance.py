"""
Global Agent Instance

Provides a singleton Agent instance for the entire application.
ton Configured as a leasing assistant with weather tools.
"""

from .openai_client import get_openai_client
from booking_agent.agent import Agent
from booking_agent.tools import TOOLS_SPEC, TOOL_IMPLS

# System prompt for leasing assistant
SYSTEM_PROMPT = """You are a helpful leasing assistant for apartment communities. 
You help potential residents with questions about apartments, amenities, and leasing.
Keep your responses friendly, concise, and professional."""

# Global agent instance
_agent_instance = None

def get_agent():
    """
    Get the global agent instance.
    Creates the agent on first call, returns cached instance on subsequent calls.
    
    Returns:
        Agent: Configured Agent instance ready for conversations
    """
    global _agent_instance
    
    if _agent_instance is None:
        client = get_openai_client()
        
        # Create agent with weather tools enabled
        _agent_instance = Agent(
            client=client,
            system_prompt=SYSTEM_PROMPT,
            tools_spec=TOOLS_SPEC,  # Include weather tools
            tool_impls=TOOL_IMPLS   # Include tool implementations
        )
    
    return _agent_instance
