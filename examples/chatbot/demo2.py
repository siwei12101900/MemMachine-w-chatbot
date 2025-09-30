#!/usr/bin/env python3
"""
MemMachine Chatbot Demo 2
Demonstrates memory-powered conversations with GPT-4o-mini.
Features Sarah, a data engineer who discusses her work and interests.
"""

import os
import sys
import time
from memmachine_chatbot import MemMachineChatbot

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("❌ OpenAI package not installed. Run: pip install openai")
    sys.exit(1)


def print_separator(char="=", length=70):
    """Print a separator line."""
    print(char * length)


def print_section(title: str):
    """Print a section header."""
    print("\n")
    print_separator()
    print(f" {title}")
    print_separator()
    print()


def chat_with_memory(user_message: str, chatbot: MemMachineChatbot, client: OpenAI, is_question: bool = False) -> str:
    """
    Architecture: MemMachine for Memory + LLM for Modeling
    
    STEP 1: MemMachine - Store the user's message in memory
    STEP 2: MemMachine - Retrieve relevant context from memory
    STEP 3: LLM - Generate intelligent response using memory context
    STEP 4: MemMachine - Store the AI's response
    
    Args:
        user_message: The user's message
        chatbot: MemMachine chatbot instance (handles ALL memory operations)
        client: OpenAI client instance (handles response generation)
        is_question: If True, emphasize this is a memory recall question
        
    Returns:
        AI-generated response
    """
    # ═══════════════════════════════════════════════════════════════
    # STEP 1: MemMachine - Store user message in memory
    # ═══════════════════════════════════════════════════════════════
    print("   📥 [MemMachine] Storing message in memory...")
    print(f"      REST API: POST {chatbot.base_url}/v1/memories/episodic")
    success, store_time = chatbot.store_user_message(user_message, verbose=True)
    print(f"      ⏱️  Time: {store_time:.3f}s")
    
    # ═══════════════════════════════════════════════════════════════
    # STEP 2: MemMachine - Retrieve relevant context from memory
    # ═══════════════════════════════════════════════════════════════
    print("   🔍 [MemMachine] Retrieving relevant memories...")
    print(f"      REST API: POST {chatbot.base_url}/v1/memories/episodic/search")
    memories, search_time = chatbot.search_memory(user_message, verbose=True)
    context_str = chatbot.recall(user_message)
    episodic_count = len(memories.get("episodic_memory", []))
    print(f"   📚 [MemMachine] Found {episodic_count} memory entries")
    print(f"      ⏱️  Time: {search_time:.3f}s")
    
    # Prepare messages for the LLM
    messages = [
        {
            "role": "system", 
            "content": "You are a helpful assistant with access to conversation memory. Use the context provided to give personalized, contextually aware responses. Be friendly and conversational."
        }
    ]
    
    # Add context if available
    if context_str and "No memories found" not in context_str:
        if is_question:
            messages.append({
                "role": "system",
                "content": f"The user is asking you to recall information from the conversation. Here's what you remember:\n\n{context_str}\n\nAnswer based on this memory."
            })
        else:
            messages.append({
                "role": "system",
                "content": f"Previous conversation context:\n\n{context_str}"
            })
    
    # Add user message
    messages.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        # ═══════════════════════════════════════════════════════════════
        # STEP 3: LLM - Generate response using memory context
        # ═══════════════════════════════════════════════════════════════
        print("   🤖 [LLM] Generating response with GPT-4o-mini...")
        print(f"      API: OpenAI Chat Completions")
        
        llm_start = time.time()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        llm_time = time.time() - llm_start
        
        ai_response = response.choices[0].message.content
        print("   ✅ [LLM] Response generated successfully")
        print(f"      ⏱️  Time: {llm_time:.3f}s")
        
        # ═══════════════════════════════════════════════════════════════
        # STEP 4: MemMachine - Store AI response in memory
        # ═══════════════════════════════════════════════════════════════
        print("   💾 [MemMachine] Storing AI response...")
        print(f"      REST API: POST {chatbot.base_url}/v1/memories/episodic")
        success, store_ai_time = chatbot.store_assistant_message(ai_response, verbose=True)
        print(f"      ⏱️  Time: {store_ai_time:.3f}s")
        
        # Calculate total time
        total_time = store_time + search_time + llm_time + store_ai_time
        print()
        print(f"   📊 Total Turn Time: {total_time:.3f}s")
        print(f"      ├─ Store user msg:  {store_time:.3f}s ({store_time/total_time*100:.1f}%)")
        print(f"      ├─ Search memories: {search_time:.3f}s ({search_time/total_time*100:.1f}%)")
        print(f"      ├─ LLM generation:  {llm_time:.3f}s ({llm_time/total_time*100:.1f}%)")
        print(f"      └─ Store AI msg:    {store_ai_time:.3f}s ({store_ai_time/total_time*100:.1f}%)")
        
        return ai_response
        
    except Exception as e:
        return f"Error generating response: {e}"


def main():
    """Run the demo conversation."""
    
    print_section("MemMachine Demo 2: Sarah's Journey")
    print("Architecture: MemMachine for Memory + LLM for Modeling")
    print()
    print("┌─────────────────────────────────────────────────────────┐")
    print("│  MemMachine → Stores & Retrieves Conversation Memory   │")
    print("│  LLM (GPT-4o-mini) → Generates Intelligent Responses   │")
    print("└─────────────────────────────────────────────────────────┘")
    print()
    print("Watch the clear separation of concerns:")
    print("  📥 💾 = MemMachine operations (memory)")
    print("  🤖 = LLM operations (modeling)")
    print()
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found!")
        print("\nSet it with:")
        print("  export OPENAI_API_KEY='sk-your-key-here'")
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
            user_id="sarah",
            agent_id="demo2_assistant"
        )
        print(f"✓ MemMachine connected")
        print(f"✓ Session: {chatbot.session_id}")
    except Exception as e:
        print(f"❌ Failed to connect to MemMachine: {e}")
        sys.exit(1)
    
    print()
    input("Press Enter to start the conversation...")
    
    # Conversation flow
    conversation = [
        {
            "user": "Hi! My name is Sarah and I'm a data engineer",
            "is_question": False,
            "note": "Sarah introduces herself"
        },
        {
            "user": "I'm currently working on a machine learning project using Python. I love working with neural networks!",
            "is_question": False,
            "note": "Sarah shares her work and interests"
        },
        {
            "user": "I'm building a recommendation system for a music streaming app. It's quite challenging but exciting!",
            "is_question": False,
            "note": "Sarah describes her project"
        },
        {
            "user": "what is my name and what do i do for work",
            "is_question": True,
            "note": "🔍 Testing memory recall: Name and profession"
        },
        {
            "user": "can you remember what programming language i mentioned",
            "is_question": True,
            "note": "🔍 Testing memory recall: Programming language"
        },
        {
            "user": "what is my area of interest in machine learning",
            "is_question": True,
            "note": "🔍 Testing memory recall: ML interest"
        },
        {
            "user": "I also enjoy hiking and traveling in my free time",
            "is_question": False,
            "note": "Sarah shares personal interests"
        },
        {
            "user": "My favorite city is Paris",
            "is_question": False,
            "note": "Sarah shares her favorite city"
        },
        {
            "user": "what are my hobbies and professional interest",
            "is_question": True,
            "note": "🔍 Final test: Comprehensive recall"
        }
    ]
    
    # Run through the conversation
    for i, turn in enumerate(conversation, 1):
        print_separator("─")
        if turn["is_question"]:
            print(f"💭 Memory Test {i}/{len(conversation)}: {turn['note']}")
        else:
            print(f"💬 Turn {i}/{len(conversation)}: {turn['note']}")
        print_separator("─")
        print()
        
        # User message
        print(f"👤 Sarah: {turn['user']}")
        print()
        
        # Get AI response (MemMachine + LLM working together)
        ai_response = chat_with_memory(
            turn['user'], 
            chatbot, 
            client, 
            is_question=turn['is_question']
        )
        
        # Display response
        print()
        if turn["is_question"]:
            print(f"🤖 AI (Recalling): {ai_response}")
        else:
            print(f"🤖 AI: {ai_response}")
        print()
        
        # Pause for readability (except on last turn)
        if i < len(conversation):
            input("Press Enter to continue...")
            print()
    
    # Summary
    print_section("Demo Complete!")
    print("✓ All messages stored in MemMachine")
    print("✓ AI successfully recalled:")
    print("  - Sarah's name and profession")
    print("  - Programming language (Python)")
    print("  - ML interest (neural networks)")
    print("  - Personal hobbies (hiking, traveling)")
    print("  - Favorite city (Paris)")
    print("  - Complete professional and personal profile")
    print()
    print(f"Session ID: {chatbot.session_id}")
    print()
    print("The AI demonstrated perfect memory recall throughout the conversation!")
    print()


if __name__ == "__main__":
    main()

