# prompts/base_prompt.py
import json
import logging
import time
import uuid
from typing import List, Dict, Optional
from abc import ABC
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from schemas import BookingResponse

# Set up logger for this module
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class BasePrompt(ABC):
    """
    Base class for all prompts that can be executed by an agent.
    Always returns structured output (BookingResponse).
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
    
    def execute(self, agent, msgs: List[Dict[str, str]], request_id: str = None) -> BookingResponse:
        """
        Execute the prompt using the provided agent.
        Agent provides clean message list, prompt just adds its content and handles API calls.
        Always returns structured output (BookingResponse).
        """
        if request_id is None:
            request_id = str(uuid.uuid4())[:8]  # Fallback to short random ID
        else:
            request_id = request_id[:8] if len(request_id) > 8 else request_id  # Truncate for logs
        start_time = time.perf_counter()
        
        logger.info(f"🎯 [{request_id}] {self.__class__.__name__} | msgs={len(msgs)} tools={self.requires_tools}")
        
        # Add current prompt to the clean message list provided by Agent
        msgs.append({"role": "user", "content": self.prompt_text})
        
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
        
        # First LLM call with timing
        llm1_start = time.perf_counter()
        r1 = agent.client.chat.completions.create(**api_params)
        llm1_time = time.perf_counter() - llm1_start
        
        # Log token usage if available
        usage1 = getattr(r1, 'usage', None)
        if usage1:
            logger.info(f"🤖 [{request_id}] LLM1 | {llm1_time:.3f}s | tokens: {usage1.prompt_tokens}→{usage1.completion_tokens} (total: {usage1.total_tokens})")
        else:
            logger.info(f"🤖 [{request_id}] LLM1 | {llm1_time:.3f}s | tokens: unavailable")
        
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
                tool_start = time.perf_counter()
                name = call.function.name
                args = json.loads(call.function.arguments or "{}")
                if name not in agent.tool_impls:
                    raise ValueError(f"Unknown function: {name}")
                out = agent.tool_impls[name](**args)
                tool_time = time.perf_counter() - tool_start
                
                # Log tool execution with response
                logger.info(f"🔧 [{request_id}] {name} | {tool_time:.3f}s | args={args} | response={out}")
                
                # Add tool call result to messages
                msgs.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": name,
                    "content": json.dumps(out),
                })
        
        # Final API call with structured output (whether tools were used or not)
        llm2_start = time.perf_counter()
        response = agent.client.beta.chat.completions.parse(
            model=agent._model,
            messages=msgs,
            response_format=BookingResponse,
            temperature=agent._temperature,
            max_tokens=agent._max_output_tokens
        )
        llm2_time = time.perf_counter() - llm2_start
        
        # Log final LLM call
        usage2 = getattr(response, 'usage', None)
        if usage2:
            logger.info(f"🤖 [{request_id}] LLM2 | {llm2_time:.3f}s | tokens: {usage2.prompt_tokens}→{usage2.completion_tokens} (total: {usage2.total_tokens})")
        else:
            logger.info(f"🤖 [{request_id}] LLM2 | {llm2_time:.3f}s | tokens: unavailable")
        
        result = response.choices[0].message.parsed
        total_time = time.perf_counter() - start_time
        
        logger.info(f"✅ [{request_id}] Complete | {total_time:.3f}s | action={result.action}")
        return result


class ToolPrompt(BasePrompt):
    """A prompt that requires tool calls. Minimal extension of BasePrompt."""
    
    def __init__(self, prompt_text: str, context: Optional[Dict] = None):
        super().__init__(prompt_text, requires_tools=True, context=context)
