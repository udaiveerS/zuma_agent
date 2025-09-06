# prompts/router_prompt.py
from ..base_prompt import BasePrompt
from enum import Enum
from typing import Optional, List, Dict
import logging
import json

# Set up logger for this module
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ConversationType(Enum):
    NORMAL_CONVO = "NORMAL_CONVO"
    GET_PROPERTY_INFO = "GET_PROPERTY_INFO"

class RouterPrompt(BasePrompt):
    """Router prompt that classifies user intent and forwards to appropriate prompt."""
    
    def __init__(self, user_query: str, context: Optional[Dict] = None):
        self.original_query = user_query
        # Classification prompt
        # Build context information for classification using JSON
        context_info = ""
        if context:
            # Filter out None values and format as JSON
            clean_context = {k: v for k, v in context.items() if v is not None}
            if clean_context:
                context_info = f"\n\nUser Context:\n{json.dumps(clean_context, indent=2)}"
        
        classification_prompt = f"""
Analyze the following user query and determine the conversation type.

User query: "{user_query}"{context_info}

Respond with EXACTLY one of these options:
- NORMAL_CONVO: For general conversation, greetings, questions, or any non-property related topics
- GET_PROPERTY_INFO: For property/unit availability queries, pricing questions, apartment/unit inquiries, move-in questions, lease questions, pet policy questions

Only respond with the classification, nothing else.

Classification:"""
        
        # Router itself doesn't need tools for classification
        super().__init__(classification_prompt, requires_tools=False, context=context)
    
    def execute(self, agent, msgs: List[Dict[str, str]]) -> str:
        """
        Execute routing: classify intent and forward to appropriate prompt.
        """
        logger.info(f"🔀 ROUTER: Starting classification for query: '{self.original_query}'")
        logger.info(f"🔀 ROUTER: Input message history has {len(msgs)} messages")
        
        # Step 1: Add classification prompt to conversation flow
        msgs.append({"role": "user", "content": self.prompt_text})
        logger.info(f"🔀 ROUTER: Added classification prompt to conversation (total: {len(msgs)})")
        
        # Get classification using direct API call
        logger.info("🔀 ROUTER: Calling OpenAI for classification...")
        r1 = agent.client.chat.completions.create(
            model=agent._model,
            messages=msgs,
            temperature=agent._temperature,
            max_tokens=agent._max_output_tokens,
        )
        classification_response = r1.choices[0].message.content
        conversation_type = self._parse_response(classification_response)
        
        logger.info(f"🔀 ROUTER: Classification result: {classification_response.strip()}")
        logger.info(f"🔀 ROUTER: Parsed as: {conversation_type}")
        
        # Step 2: Add classification response to conversation history
        msgs.append({"role": "assistant", "content": f"[ROUTING: {conversation_type.value}]"})
        logger.info(f"🔀 ROUTER: Added routing decision to conversation history (total: {len(msgs)})")
        
        # Step 2: Forward to appropriate prompt based on classification using updated msgs
        if conversation_type == ConversationType.GET_PROPERTY_INFO:
            logger.info("🏠 ROUTER: Forwarding to GetPropertyInfoPrompt")
            from .get_property_info import GetPropertyInfoPrompt
            property_prompt = GetPropertyInfoPrompt(self.original_query, context=self.context)
            result = property_prompt.execute(agent, msgs)
            logger.info(f"🏠 ROUTER: GetPropertyInfoPrompt returned: {result[:100]}...")
            return result
        else:  # NORMAL_CONVO
            logger.info("💬 ROUTER: Forwarding to FriendlyChatPrompt")
            from .friendly_chat_prompt import FriendlyChatPrompt
            chat_prompt = FriendlyChatPrompt(self.original_query, context=self.context)
            result = chat_prompt.execute(agent, msgs)
            logger.info(f"💬 ROUTER: FriendlyChatPrompt returned: {result[:100]}...")
            return result
    
    def _parse_response(self, response: str) -> ConversationType:
        """Parse the router response and return the conversation type."""
        response = response.strip().upper()
        
        if "GET_PROPERTY_INFO" in response:
            return ConversationType.GET_PROPERTY_INFO
        elif "NORMAL_CONVO" in response:
            return ConversationType.NORMAL_CONVO
        else:
            # Default to normal conversation if unclear
            return ConversationType.NORMAL_CONVO
