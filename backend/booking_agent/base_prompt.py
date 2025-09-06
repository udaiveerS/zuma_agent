# base_prompt.py
import json
import logging
from typing import List, Dict, Optional
from abc import ABC

# Set up logger for this module
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class BasePrompt(ABC):
    """
    Base class for all prompts that can be executed by an agent.
    """
    
    def __init__(self, prompt_text: str, requires_tools: bool = False, context: Optional[Dict] = None):
        """
        Initialize the prompt.
        
        Args:
            prompt_text: The prompt string to send to the model
            requires_tools: Whether this prompt expects/allows tool calls
            context: Optional context dict with user preferences, community_id, etc.
        """
        self.prompt_text = prompt_text
        self.requires_tools = requires_tools
        self.context = context or {}
    
    def execute(self, agent, msgs: List[Dict[str, str]]) -> str:
        """
        Execute the prompt using the provided agent.
        Agent provides clean message list, prompt just adds its content and handles API calls.
        """
        logger.info(f"📝 PROMPT: Executing {self.__class__.__name__}")
        logger.info(f"📝 PROMPT: Input messages: {len(msgs)}, Requires tools: {self.requires_tools}")
        
        # Add current prompt to the clean message list provided by Agent
        msgs.append({"role": "user", "content": self.prompt_text})
        logger.info(f"📝 PROMPT: Added prompt text, total messages: {len(msgs)}")
        
        # First API call
        api_params = {
            "model": agent._model,
            "messages": msgs,
            "temperature": agent._temperature,
            "max_tokens": agent._max_output_tokens,
        }
        
        # Only add tool parameters if tools are required
        if self.requires_tools and agent.tools_spec:
            api_params["tools"] = agent.tools_spec
            api_params["tool_choice"] = agent._tool_choice
        
        r1 = agent.client.chat.completions.create(**api_params)
        
        # If this prompt doesn't require tools, return immediately
        if not self.requires_tools:
            response = r1.choices[0].message.content
            logger.info(f"📝 PROMPT: OpenAI response (no tools): {response[:100]}...")
            return response
        
        # Handle tool calls if required
        tool_calls = r1.choices[0].message.tool_calls or []
        
        if tool_calls:
            # First add the assistant's message with tool calls
            msgs.append({
                "role": "assistant",
                "content": r1.choices[0].message.content,
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments
                        }
                    } for call in tool_calls
                ]
            })
            
            # Then add tool responses
            for call in tool_calls:
                name = call.function.name
                args = json.loads(call.function.arguments or "{}")
                if name not in agent.tool_impls:
                    raise ValueError(f"Unknown function: {name}")
                out = agent.tool_impls[name](**args)
                
                # Add tool call result to messages
                msgs.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": name,
                    "content": json.dumps(out),
                })
            
            # Second API call with tool results
            r2 = agent.client.chat.completions.create(
                model=agent._model,
                messages=msgs,
                tools=agent.tools_spec,
                temperature=agent._temperature,
                max_tokens=agent._max_output_tokens,
                tool_choice=agent._tool_choice,
            )
            return r2.choices[0].message.content
        
        # No tools were called
        return r1.choices[0].message.content


class SimplePrompt(BasePrompt):
    """A simple prompt that doesn't require tools."""
    
    def __init__(self, prompt_text: str, context: Optional[Dict] = None):
        super().__init__(prompt_text, requires_tools=False, context=context)


class ToolPrompt(BasePrompt):
    """A prompt that may require tool calls."""
    
    def __init__(self, prompt_text: str, context: Optional[Dict] = None):
        super().__init__(prompt_text, requires_tools=True, context=context)


class ChatPrompt(SimplePrompt):
    """Specific prompt for simple chat interactions."""
    
    def __init__(self, message: str, context: Optional[Dict] = None):
        super().__init__(message, context=context)
