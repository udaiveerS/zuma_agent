# agent/agent.py
import json
from typing import List, Dict, Callable
from .response.agent_response import AgentResponse
from .base_prompt import BasePrompt

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

        # Speed-optimized config
        self._model = "gpt-4o-mini"  # Fastest GPT-4 model
        self._temperature = 0.0      # Fastest (no randomness)
        self._max_output_tokens = 150  # Shorter responses = faster
        self._tool_choice = "auto"


    def run(self, user_prompt: BasePrompt, conversation_history: List[Dict[str, str]] = None) -> AgentResponse:
        """
        Execute a prompt using this agent.
        Returns: AgentResponse with response text and clean conversation history
        """
        # Build clean message list - Agent's responsibility
        msgs = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation history if provided (filter system messages for security)
        if conversation_history:
            filtered_history = [msg for msg in conversation_history if msg.get("role") != "system"]
            msgs.extend(filtered_history)
        
        # Execute the prompt (user_prompt is guaranteed to be BasePrompt)
        response_text = user_prompt.execute(self, msgs)
        
        # Create and return AgentResponse object (no history cleaning)
        return AgentResponse(
            response=response_text,
            conversation_history=conversation_history,  # Return original history as-is
            metadata={
                'model': self._model,
                'temperature': self._temperature,
                'system_prompt_length': len(self.system_prompt)
            }
        )