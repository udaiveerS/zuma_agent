# main.py
import os
from dotenv import load_dotenv
from openai import OpenAI

from agent import Agent
from tools import TOOLS_SPEC, TOOL_IMPLS
from prompts.router_prompt import RouterPrompt
from response.agent_response import AgentResponse

load_dotenv()  # expects OPENAI_API_KEY in .env

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = "You are a helpful and concise assistant."

agent = Agent(
    client=client,
    system_prompt=SYSTEM_PROMPT,
    tools_spec=TOOLS_SPEC,
    tool_impls=TOOL_IMPLS,
)

def chat_with_agent(user_input: str, conversation_history: list = None) -> AgentResponse:
    """Simple function to chat with the agent."""
    router = RouterPrompt(user_input)
    return agent.run(router, conversation_history)

if __name__ == "__main__":
    print("🤖 INTERACTIVE CHAT WITH AGENT")
    print("=" * 40)
    print("Type 'quit', 'exit', or 'bye' to end the conversation")
    print("Type 'history' to see conversation history")
    print("Type 'clear' to clear conversation history")
    print("-" * 40)
    
    conversation_history = None
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            # Check for special commands
            if user_input.lower() == 'history':
                if conversation_history:
                    print("\n📋 Conversation History:")
                    for i, msg in enumerate(conversation_history, 1):
                        print(f"  {i}. {msg['role']}: {msg['content']}")
                else:
                    print("📋 No conversation history yet.")
                continue
            
            if user_input.lower() == 'clear':
                conversation_history = None
                print("🗑️  Conversation history cleared!")
                continue
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Get response from agent
            response = chat_with_agent(user_input, conversation_history)
            
            # Update conversation history for next turn
            conversation_history = response.conversation_history
            
            # Show agent response
            print(f"🤖 Agent: {response.response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again.")
    
    print("\n✅ Chat session ended.")

