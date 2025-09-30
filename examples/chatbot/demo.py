#!/usr/bin/env python3
"""
MemMachine Chatbot Demo
A demonstration of the MemMachine chatbot with conversation and memory recall.
"""

import os
import sys
import time
from memmachine_chatbot import MemMachineChatbot


def print_separator(char="=", length=60):
    """Print a separator line."""
    print(char * length)


def print_section(title: str):
    """Print a section header."""
    print("\n")
    print_separator()
    print(f" {title}")
    print_separator()
    print()


def demo_conversation():
    """Run a demo conversation with memory storage and recall."""
    
    # Configuration - can be changed via environment variables
    api_url = os.getenv("MEMMACHINE_URL", "http://localhost:8080")
    user_id = os.getenv("USER_ID", "demo_user")
    
    print_section("MemMachine Chatbot Demo")
    print(f"API URL: {api_url}")
    print(f"User ID: {user_id}")
    print()
    
    # Initialize chatbot
    try:
        chatbot = MemMachineChatbot(
            base_url=api_url,
            user_id=user_id,
            agent_id="demo_assistant"
        )
        print(f"✓ Chatbot initialized with session: {chatbot.session_id}\n")
    except Exception as e:
        print(f"✗ Failed to initialize chatbot: {e}")
        print("\nMake sure MemMachine is running at:", api_url)
        print("You can start it with: docker-compose up")
        sys.exit(1)
    
    # Simulate a conversation
    print_section("Phase 1: Building Conversation Memory")
    
    conversations = [
        {
            "user": "Hi! My name is Alice and I'm a software engineer.",
            "assistant": "Hello Alice! Nice to meet you. It's great to connect with a fellow software engineer. What kind of projects are you working on?"
        },
        {
            "user": "I'm currently working on a machine learning project using Python. I love working with neural networks!",
            "assistant": "That's fantastic! Machine learning and neural networks are fascinating fields. Python is an excellent choice for ML work with libraries like TensorFlow and PyTorch. What specific problem are you trying to solve with your neural network?"
        },
        {
            "user": "I'm building a recommendation system for a music streaming app. It's quite challenging but exciting!",
            "assistant": "A music recommendation system sounds like a really cool project! Recommendation systems are complex but incredibly rewarding when they work well. Are you using collaborative filtering, content-based filtering, or a hybrid approach?"
        },
        {
            "user": "I'm using a hybrid approach. By the way, my favorite music genre is jazz.",
            "assistant": "A hybrid approach is smart - you'll get the best of both worlds! And jazz is wonderful - such rich harmonies and improvisation. That must give you interesting insights into what makes good recommendations for jazz listeners."
        }
    ]
    
    # Store conversations in memory
    for i, conv in enumerate(conversations, 1):
        print(f"Turn {i}:")
        print(f"  User: {conv['user']}")
        
        # Store user message
        success = chatbot.store_user_message(conv['user'])
        if success:
            print("    ✓ User message stored in memory")
        else:
            print("    ✗ Failed to store user message")
        
        time.sleep(0.5)  # Small delay for readability
        
        print(f"  Assistant: {conv['assistant']}")
        
        # Store assistant message
        success = chatbot.store_assistant_message(conv['assistant'])
        if success:
            print("    ✓ Assistant message stored in memory")
        else:
            print("    ✗ Failed to store assistant message")
        
        print()
        time.sleep(0.5)
    
    # Test memory recall
    print_section("Phase 2: Testing Memory Recall")
    
    recall_queries = [
        "What is my name?",
        "What do I do for work?",
        "What project am I working on?",
        "What is my favorite music genre?",
        "What technology am I using?"
    ]
    
    for query in recall_queries:
        print(f"🔍 Query: {query}")
        print()
        
        recalled = chatbot.recall(query)
        print("📝 Recalled memories:")
        print(recalled)
        print()
        time.sleep(1)
    
    # Test specific memory search
    print_section("Phase 3: Advanced Memory Search")
    
    print("Searching for all messages from the user...")
    memories = chatbot.search_memory(
        query="projects and interests",
        limit=10,
        filter_params={"producer": user_id}
    )
    
    episodic = memories.get("episodic_memory", [])
    profile = memories.get("profile_memory", [])
    
    print(f"\nFound {len(episodic)} episodic memories")
    print(f"Found {len(profile)} profile entries")
    
    if episodic:
        print("\nEpisodic Memories:")
        for i, mem in enumerate(episodic[:5], 1):  # Show first 5
            print(f"  {i}. {mem}")
    
    if profile:
        print("\nProfile Information:")
        for i, prof in enumerate(profile[:5], 1):  # Show first 5
            print(f"  {i}. {prof}")
    
    # Show session info
    print_section("Phase 4: Session Information")
    
    sessions = chatbot.get_all_sessions()
    print(f"Total active sessions: {len(sessions)}")
    
    if sessions:
        print("\nSession Details:")
        for session in sessions[:3]:  # Show first 3
            print(f"  - Session ID: {session.get('session_id')}")
            print(f"    Users: {session.get('user_ids')}")
            print(f"    Agents: {session.get('agent_ids')}")
            print()
    
    # Cleanup option
    print_section("Phase 5: Cleanup (Optional)")
    
    print("This demo created a session with conversation history.")
    print(f"Session ID: {chatbot.session_id}")
    print("\nTo keep this session for testing, do nothing.")
    print("To delete this session, uncomment the cleanup code below.")
    
    # Uncomment the next two lines to enable automatic cleanup
    # print("\nDeleting session...")
    # chatbot.delete_session()
    # print("✓ Session deleted")
    
    print_section("Demo Complete!")
    print("The chatbot successfully:")
    print("  ✓ Stored conversation messages")
    print("  ✓ Recalled specific information")
    print("  ✓ Searched through memories")
    print("  ✓ Retrieved session information")
    print("\nYou can now use the MemMachineChatbot class in your own applications!")
    print()


def interactive_mode():
    """Run an interactive chatbot session."""
    
    api_url = os.getenv("MEMMACHINE_URL", "http://localhost:8080")
    user_id = os.getenv("USER_ID", "interactive_user")
    
    print_section("MemMachine Interactive Chatbot")
    print(f"API URL: {api_url}")
    print(f"User ID: {user_id}")
    print()
    
    try:
        chatbot = MemMachineChatbot(
            base_url=api_url,
            user_id=user_id,
            agent_id="interactive_assistant"
        )
        print(f"✓ Chatbot initialized with session: {chatbot.session_id}\n")
    except Exception as e:
        print(f"✗ Failed to initialize chatbot: {e}")
        sys.exit(1)
    
    print("Interactive mode ready!")
    print("Commands:")
    print("  - Type a message to store it in memory")
    print("  - Type '/recall <query>' to search memories")
    print("  - Type '/sessions' to see all sessions")
    print("  - Type '/quit' to exit")
    print()
    print_separator()
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "/quit":
                print("\nGoodbye!")
                break
            
            elif user_input.lower() == "/sessions":
                sessions = chatbot.get_all_sessions()
                print(f"\nTotal sessions: {len(sessions)}")
                for session in sessions[:5]:
                    print(f"  - {session.get('session_id')}")
                print()
            
            elif user_input.lower().startswith("/recall "):
                query = user_input[8:].strip()
                if query:
                    print(f"\n🔍 Searching for: {query}\n")
                    result = chatbot.recall(query)
                    print(result)
                    print()
                else:
                    print("Please provide a query after /recall\n")
            
            else:
                # Store the message
                success = chatbot.store_user_message(user_input)
                if success:
                    print("✓ Message stored in memory\n")
                else:
                    print("✗ Failed to store message\n")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


def main():
    """Main entry point."""
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        demo_conversation()


if __name__ == "__main__":
    main()

