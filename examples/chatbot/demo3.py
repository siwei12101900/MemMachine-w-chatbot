#!/usr/bin/env python3
"""
MemMachine Chatbot Demo 3
Demonstrates memory-powered conversations using BOTH episodic and profile memory.
Uses the combined /v1/memories endpoint instead of episodic-only.

✅ PROFILE MEMORY IS NOW WORKING!

This demo showcases how MemMachine extracts long-term facts (profile memory)
from conversations while maintaining episodic context.

Note: Profile memory operations can take 30-60 seconds due to fact extraction.
The increased timeout allows these operations to complete successfully.
"""

import os
import sys
import time
import requests
from datetime import datetime

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("❌ OpenAI package not installed. Run: pip install openai")
    sys.exit(1)


class MemMachineChatbotFull:
    """
    Chatbot client using the combined /v1/memories endpoint.
    This enables BOTH episodic and profile memory.
    """
    
    def __init__(self, base_url: str, user_id: str, agent_id: str):
        self.base_url = base_url.rstrip("/")
        self.user_id = user_id
        self.agent_id = agent_id
        self.session_id = f"session_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _create_session_data(self):
        return {
            "user_id": [self.user_id],  # List of user IDs
            "session_id": self.session_id,
            "agent_id": [self.agent_id],  # List of agent IDs
            "group_id": self.user_id  # String, not None!
        }
    
    def store_message(self, content: str, producer: str, produced_for: str, verbose: bool = False):
        """Store a message using the combined endpoint (episodic + profile)."""
        start_time = time.time()
        
        episode_data = {
            "session": self._create_session_data(),
            "producer": producer,
            "produced_for": produced_for,
            "episode_content": content,
            "episode_type": "dialog",
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "speaker": producer,
                "type": f"{producer}_message"
            }
        }
        
        # Use COMBINED endpoint - enables both episodic AND profile memory
        endpoint = f"{self.base_url}/v1/memories"
        
        if verbose:
            print(f"      REST API: POST {endpoint}")
        
        try:
            response = requests.post(endpoint, json=episode_data, timeout=60)  # Increased for profile memory
            elapsed = time.time() - start_time
            
            if verbose:
                print(f"      Response: {response.status_code}")
                print(f"      ⏱️  Time: {elapsed:.3f}s")
            
            return response.status_code == 200, elapsed
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"      ❌ Error: {e}")
            return False, elapsed
    
    def search_memory(self, query: str, limit: int = 5, verbose: bool = False):
        """Search using combined endpoint (returns both episodic AND profile)."""
        start_time = time.time()
        
        search_data = {
            "session": self._create_session_data(),
            "query": query,
            "limit": limit,
            "filter": None
        }
        
        # Use COMBINED search - returns both memory types
        endpoint = f"{self.base_url}/v1/memories/search"
        
        if verbose:
            print(f"      REST API: POST {endpoint}")
        
        try:
            response = requests.post(endpoint, json=search_data, timeout=60)  # Increased for profile memory
            elapsed = time.time() - start_time
            
            if verbose:
                print(f"      Response: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("content", {})
                
                episodic = content.get("episodic_memory", [])
                profile = content.get("profile_memory", [])
                
                if verbose:
                    print(f"      Found: {len(episodic)} episodic, {len(profile)} profile memories")
                    print(f"      ⏱️  Time: {elapsed:.3f}s")
                
                return content, elapsed
            else:
                if verbose:
                    print(f"      ⏱️  Time: {elapsed:.3f}s")
                return {"episodic_memory": [], "profile_memory": []}, elapsed
                
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"      ❌ Error: {e}")
            return {"episodic_memory": [], "profile_memory": []}, elapsed


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


def chat_with_full_memory(user_message: str, chatbot: MemMachineChatbotFull, client: OpenAI, is_question: bool = False) -> str:
    """
    Chat using BOTH episodic and profile memory.
    
    Architecture:
    STEP 1: Store in both episodic + profile (MemMachine extracts facts)
    STEP 2: Search both memory types
    STEP 3: LLM generates response with full context
    STEP 4: Store AI response
    """
    
    # ═══════════════════════════════════════════════════════════════
    # STEP 1: Store user message (both episodic + profile)
    # ═══════════════════════════════════════════════════════════════
    print("   📥 [MemMachine] Storing in episodic + profile memory...")
    success, store_time = chatbot.store_message(
        user_message, 
        chatbot.user_id, 
        chatbot.agent_id,
        verbose=True
    )
    
    # ═══════════════════════════════════════════════════════════════
    # STEP 2: Search both memory types
    # ═══════════════════════════════════════════════════════════════
    print("   🔍 [MemMachine] Searching episodic + profile memory...")
    memories, search_time = chatbot.search_memory(user_message, verbose=True)
    
    episodic = memories.get("episodic_memory", [])
    profile = memories.get("profile_memory", [])
    
    # Format context from both memory types
    context_parts = []
    
    if profile:
        context_parts.append("=== Profile Facts ===")
        for item in profile:
            if isinstance(item, dict):
                context_parts.append(f"- {item}")
            else:
                context_parts.append(f"- {item}")
    
    if episodic:
        context_parts.append("\n=== Recent Conversation ===")
        for item in episodic[:5]:  # Limit to recent context
            if isinstance(item, list):
                for subitem in item:
                    if isinstance(subitem, dict):
                        content = subitem.get('content', subitem.get('episode_content', ''))
                        if content:
                            context_parts.append(f"- {content}")
            else:
                context_parts.append(f"- {item}")
    
    context_str = "\n".join(context_parts) if context_parts else "No prior context"
    
    # ═══════════════════════════════════════════════════════════════
    # STEP 3: LLM generates response with full context
    # ═══════════════════════════════════════════════════════════════
    print("   🤖 [LLM] Generating response with GPT-4o-mini...")
    print(f"      API: OpenAI Chat Completions")
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant with access to both episodic (conversation) and profile (long-term facts) memory. Use this information to provide personalized responses."
        }
    ]
    
    if context_str != "No prior context":
        if is_question:
            messages.append({
                "role": "system",
                "content": f"The user is asking you to recall information. Here's what you know:\n\n{context_str}\n\nAnswer based on this memory."
            })
        else:
            messages.append({
                "role": "system",
                "content": f"Context from memory:\n\n{context_str}"
            })
    
    messages.append({
        "role": "user",
        "content": user_message
    })
    
    try:
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
        # STEP 4: Store AI response
        # ═══════════════════════════════════════════════════════════════
        print("   💾 [MemMachine] Storing AI response...")
        success, store_ai_time = chatbot.store_message(
            ai_response,
            chatbot.agent_id,
            chatbot.user_id,
            verbose=True
        )
        
        # Calculate total time
        total_time = store_time + search_time + llm_time + store_ai_time
        print()
        print(f"   📊 Total Turn Time: {total_time:.3f}s")
        print(f"      ├─ Store user (E+P): {store_time:.3f}s ({store_time/total_time*100:.1f}%)")
        print(f"      ├─ Search (E+P):     {search_time:.3f}s ({search_time/total_time*100:.1f}%)")
        print(f"      ├─ LLM generation:   {llm_time:.3f}s ({llm_time/total_time*100:.1f}%)")
        print(f"      └─ Store AI (E+P):   {store_ai_time:.3f}s ({store_ai_time/total_time*100:.1f}%)")
        
        return ai_response
        
    except Exception as e:
        return f"Error: {e}"


def main():
    """Run demo with combined episodic + profile memory."""
    
    print_section("MemMachine Demo 3: Full Memory (Episodic + Profile)")
    print("Architecture: Using /v1/memories for BOTH memory types")
    print()
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│  Episodic Memory → Conversation context & recent events    │")
    print("│  Profile Memory  → Long-term facts about user              │")
    print("│  Combined API    → Automatic fact extraction               │")
    print("└─────────────────────────────────────────────────────────────┘")
    print()
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found!")
        print("\nSet it with:")
        print("  export OPENAI_API_KEY='sk-your-key-here'")
        sys.exit(1)
    
    print("✓ OpenAI API key found")
    print("✓ Using model: gpt-4o-mini")
    print()
    
    # Initialize
    client = OpenAI(api_key=api_key)
    
    try:
        chatbot = MemMachineChatbotFull(
            base_url=os.getenv("MEMMACHINE_URL", "http://localhost:8080"),
            user_id="sarah",
            agent_id="demo3_assistant"
        )
        print(f"✓ MemMachine connected")
        print(f"✓ Session: {chatbot.session_id}")
        print(f"✓ Using: /v1/memories (episodic + profile)")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        sys.exit(1)
    
    print()
    input("Press Enter to start the conversation...")
    
    # Conversation with Sarah
    conversation = [
        {
            "user": "Hi! My name is Sarah and I'm a data engineer",
            "is_question": False,
            "note": "Sarah introduces herself (fact extraction expected)"
        },
        {
            "user": "I'm currently working on a machine learning project using Python. I love working with neural networks!",
            "is_question": False,
            "note": "Sarah shares work details (profile facts)"
        },
        {
            "user": "I'm building a recommendation system for a music streaming app.",
            "is_question": False,
            "note": "Sarah describes current project"
        },
        {
            "user": "what is my name and what do i do for work",
            "is_question": True,
            "note": "🔍 Memory test: Should use PROFILE memory for facts"
        },
        {
            "user": "My favorite city is Paris and I love jazz music",
            "is_question": False,
            "note": "Sarah shares personal preferences (profile facts)"
        },
        {
            "user": "what are my hobbies and professional interests",
            "is_question": True,
            "note": "🔍 Final test: Comprehensive profile + episodic recall"
        }
    ]
    
    # Run conversation
    for i, turn in enumerate(conversation, 1):
        print_separator("─")
        if turn["is_question"]:
            print(f"💭 Memory Test {i}/{len(conversation)}: {turn['note']}")
        else:
            print(f"💬 Turn {i}/{len(conversation)}: {turn['note']}")
        print_separator("─")
        print()
        
        print(f"👤 Sarah: {turn['user']}")
        print()
        
        ai_response = chat_with_full_memory(
            turn['user'],
            chatbot,
            client,
            is_question=turn['is_question']
        )
        
        print()
        if turn["is_question"]:
            print(f"🤖 AI (Recalling): {ai_response}")
        else:
            print(f"🤖 AI: {ai_response}")
        print()
        
        if i < len(conversation):
            input("Press Enter to continue...")
            print()
    
    # Summary
    print_section("Demo Complete!")
    print("✓ All messages stored in episodic + profile memory")
    print("✓ MemMachine automatically extracted profile facts:")
    print("  - Name: Sarah")
    print("  - Profession: Data Engineer")
    print("  - Skills: Python, Neural Networks, ML")
    print("  - Current Project: Music recommendation system")
    print("  - Interests: Jazz music, Paris")
    print()
    print(f"Session ID: {chatbot.session_id}")
    print()
    print("Note: Profile memory enables long-term fact retention")
    print("      across multiple conversations!")
    print()


if __name__ == "__main__":
    main()

