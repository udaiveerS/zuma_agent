# agent/agent.py
import json
from typing import List, Dict, Callable
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from schemas import BookingResponse
from .prompts.base_prompt import BasePrompt

class Agent:
    """
    Minimal Agent:
      - injects a system prompt
      - declares tools exactly as provided
      - first pass: model may request tool(s)
      - run tool(s), append outputs
      - second pass: final text
    """
    def __init__(self, client, system_prompt: str, tools_spec: List[Dict], tool_impls: Dict[str, Callable]):
        self.client = client
        self.system_prompt = system_prompt
        self.tools_spec = tools_spec
        self.tool_impls = tool_impls

        # Speed-optimized config with some variety
        self._model = "gpt-4o-mini"  # Fastest GPT-4 model
        self._temperature = 0.2      # Low randomness - safe for structured output
        self._max_output_tokens = 150  # Shorter responses = faster
        self._tool_choice = "auto"


    def run(self, user_prompt, conversation_history: List[Dict[str, str]] = None, request_id: str = None) -> BookingResponse:
        """
        Execute a prompt using this agent.
        Returns: BookingResponse directly
        """
        # Build clean message list - Agent's responsibility
        msgs = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation history if provided (filter system messages for security)
        if conversation_history:
            filtered_history = [msg for msg in conversation_history if msg.get("role") != "system"]
            msgs.extend(filtered_history)
        
        # Execute the prompt and return BookingResponse directly
        booking_response = user_prompt.execute(self, msgs, request_id=request_id)
        return booking_response