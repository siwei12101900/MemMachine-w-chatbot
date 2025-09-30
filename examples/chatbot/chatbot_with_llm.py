#!/usr/bin/env python3
"""
MemMachine Chatbot with LLM Integration
This example shows how to add AI-powered responses using OpenAI GPT-4o-mini.
"""

import os
import sys
from memmachine_chatbot import MemMachineChatbot

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI package not installed. Run: pip install openai")


def chat_with_llm(user_message: str, chatbot: MemMachineChatbot, client: 'OpenAI') -> str:
    """
    Generate an AI response using OpenAI GPT-4o-mini and MemMachine memory.
    
    Args:
        user_message: The user's message
        chatbot: MemMachine chatbot instance
        client: OpenAI client instance
        
    Returns:
        AI-generated response
    """
    # Get relevant memories for context
    context = chatbot.recall(user_message)
    
    # Prepare messages for the LLM
    messages = [
        {
            "role": "system", 
            "content": "You are a helpful assistant with access to conversation memory. Use the context provided to give personalized, contextually aware responses."
        }
    ]
    
    # Add context if available
    if context and "No memories found" not in context:
        messages.append({
            "role": "system",
            "content": f"Here's what you remember from previous conversations:\n\n{context}"
        })
    
    # Add user message
    messages.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        # Call OpenAI API with GPT-4o-mini
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error generating response: {e}"


def main():
    """Run an interactive chatbot with GPT-4o-mini integration."""
    
    print("=" * 70)
    print(" MemMachine Chatbot with GPT-4o-mini")
    print("=" * 70)
    print()
    
    # Check if OpenAI package is available
    if not OPENAI_AVAILABLE:
        print("❌ OpenAI package not installed!")
        print("\nInstall it with:")
        print("  pip install openai")
        print()
        sys.exit(1)
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found!")
        print("\nSet it with:")
        print("  export OPENAI_API_KEY='sk-your-key-here'")
        print("\nOr get a key at: https://platform.openai.com/api-keys")
        print()
        sys.exit(1)
    
    print("✓ OpenAI API key found")
    print("✓ Using model: gpt-4o-mini")
    print()
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Initialize MemMachine chatbot
    try:
        chatbot = MemMachineChatbot(
            base_url=os.getenv("MEMMACHINE_URL", "http://localhost:8080"),
            user_id=os.getenv("USER_ID", "llm_user"),
            agent_id="gpt4o_mini_assistant"
        )
        print(f"✓ MemMachine connected")
        print(f"✓ Session: {chatbot.session_id}")
    except Exception as e:
        print(f"❌ Failed to connect to MemMachine: {e}")
        print("\nMake sure MemMachine is running at:")
        print(f"  {os.getenv('MEMMACHINE_URL', 'http://localhost:8080')}")
        sys.exit(1)
    
    print()
    print("Ready to chat! The AI has access to conversation memory.")
    print()
    print("Commands:")
    print("  - Type a message to chat with GPT-4o-mini")
    print("  - Type '/quit' to exit")
    print()
    print("=" * 70)
    print()
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["/quit", "/exit", "quit", "exit"]:
                print("\nGoodbye!")
                break
            
            # Store user message in MemMachine
            chatbot.store_user_message(user_input)
            print("  💾 Stored in memory...")
            
            # Generate AI response using GPT-4o-mini with memory context
            print("  🤔 Thinking...")
            ai_response = chat_with_llm(user_input, chatbot, client)
            
            # Store AI response in MemMachine
            chatbot.store_assistant_message(ai_response)
            
            # Display response
            print(f"\nAI: {ai_response}")
            print()
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()

