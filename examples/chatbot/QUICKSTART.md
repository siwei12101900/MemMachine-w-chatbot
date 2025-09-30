# MemMachine Chatbot - Quick Start Guide

Get your chatbot running in 3 minutes!

## Prerequisites

✅ Python 3.8 or higher  
✅ MemMachine server running (default: http://localhost:8080)

## Step 1: Install Dependencies

```bash
cd examples/chatbot
pip install -r requirements.txt
```

## Step 2: Verify MemMachine is Running

Check if the MemMachine API is accessible:

```bash
curl http://localhost:8080/v1/health
```

You should see a response like:
```json
{
  "status": "healthy",
  "service": "memmachine",
  ...
}
```

**If MemMachine is not running:**

```bash
# Option 1: Using Docker Compose (from project root)
docker-compose up

# Option 2: Using Python (from project root)
cd src
python -m memmachine.server.app
```

## Step 3: Run the Demo

### Automated Demo

Watch a pre-programmed conversation with memory recall:

```bash
python demo.py
```

This will:
- ✅ Store a 4-turn conversation about Alice (a software engineer)
- ✅ Recall specific facts (name, job, project, interests)
- ✅ Show episodic and profile memories
- ✅ Display session information

Expected output:
```
================================================================
 MemMachine Chatbot Demo
================================================================

API URL: http://localhost:8080
User ID: demo_user

✓ Chatbot initialized with session: session_demo_user_20240130_143052

================================================================
 Phase 1: Building Conversation Memory
================================================================

Turn 1:
  User: Hi! My name is Alice and I'm a software engineer.
    ✓ User message stored in memory
  Assistant: Hello Alice! Nice to meet you...
    ✓ Assistant message stored in memory

...

================================================================
 Phase 2: Testing Memory Recall
================================================================

🔍 Query: What is my name?

📝 Recalled memories:
=== Conversation History ===
user: Hi! My name is Alice and I'm a software engineer.
...
```

### Interactive Mode

Start a live chat session:

```bash
python demo.py --interactive
```

Try these commands:
```
You: My name is Bob and I love Python programming
✓ Message stored in memory

You: I'm working on a machine learning project
✓ Message stored in memory

You: /recall What is my name?
🔍 Searching for: What is my name?

📝 Recalled memories:
=== Conversation History ===
user: My name is Bob and I love Python programming
...

You: /sessions
Total sessions: 3
  - session_interactive_user_20240130_143152
  ...

You: /quit
Goodbye!
```

## Step 4: Use in Your Code

### Basic Example

Create a file called `my_chatbot.py`:

```python
from memmachine_chatbot import MemMachineChatbot

# Initialize
chatbot = MemMachineChatbot(
    base_url="http://localhost:8080",
    user_id="alice"
)

# Store messages
chatbot.store_user_message("Hi! I love Python.")
chatbot.store_assistant_message("That's great! Python is versatile.")
chatbot.store_user_message("I'm learning machine learning.")

# Recall information
result = chatbot.recall("What is the user learning?")
print(result)
```

Run it:
```bash
python my_chatbot.py
```

### With Custom Configuration

```python
import os
from memmachine_chatbot import MemMachineChatbot

# Use environment variables for configuration
chatbot = MemMachineChatbot(
    base_url=os.getenv("MEMMACHINE_URL", "http://localhost:8080"),
    user_id=os.getenv("USER_ID", "default_user"),
    agent_id="my_awesome_agent"
)

# Your chatbot logic here...
```

## Configuration Options

### Environment Variables

```bash
# Set custom API URL
export MEMMACHINE_URL="http://your-server:8080"

# Set custom user ID
export USER_ID="your_user_id"

# Run demo with custom configuration
python demo.py
```

### Python Code

```python
chatbot = MemMachineChatbot(
    base_url="http://localhost:8080",   # MemMachine API URL
    user_id="alice",                    # User identifier
    session_id="custom_session_123",    # Optional: auto-generated if not provided
    agent_id="my_assistant"             # Agent identifier
)
```

## Common Use Cases

### 1. Simple Q&A Bot

```python
from memmachine_chatbot import MemMachineChatbot

def qa_bot(user_id):
    chatbot = MemMachineChatbot(user_id=user_id)
    
    while True:
        question = input("Ask me anything (or 'quit'): ")
        if question.lower() == 'quit':
            break
        
        # Store the question
        chatbot.store_user_message(question)
        
        # Get context from memory
        context = chatbot.recall(question)
        
        # Generate answer (integrate with your LLM here)
        answer = f"Based on what I remember:\n{context}"
        
        # Store the answer
        chatbot.store_assistant_message(answer)
        
        print(answer)

qa_bot("user123")
```

### 2. Conversation Logger

```python
from memmachine_chatbot import MemMachineChatbot

def log_conversation(user_id, conversation_pairs):
    chatbot = MemMachineChatbot(user_id=user_id)
    
    for user_msg, assistant_msg in conversation_pairs:
        chatbot.store_user_message(user_msg)
        chatbot.store_assistant_message(assistant_msg)
    
    print(f"✓ Logged {len(conversation_pairs)} conversation turns")

# Example usage
log_conversation("alice", [
    ("Hello!", "Hi there!"),
    ("How are you?", "I'm doing well, thanks!"),
    ("Great!", "Glad to hear it!")
])
```

### 3. Memory-Enhanced Search

```python
from memmachine_chatbot import MemMachineChatbot

def smart_search(user_id, queries):
    chatbot = MemMachineChatbot(user_id=user_id)
    
    for query in queries:
        print(f"\n🔍 Searching: {query}")
        
        memories = chatbot.search_memory(
            query=query,
            limit=5,
            filter_params={"producer": user_id}
        )
        
        print(f"Found {len(memories.get('episodic_memory', []))} relevant memories")

# Example usage
smart_search("bob", [
    "programming languages",
    "favorite hobbies",
    "work projects"
])
```

## Troubleshooting

### "Failed to connect to MemMachine API"

**Solution**: Make sure MemMachine is running
```bash
# Check health
curl http://localhost:8080/v1/health

# Start MemMachine if needed
docker-compose up
```

### "Failed to store message"

**Solution**: Check MemMachine logs for errors
```bash
# If using Docker
docker-compose logs -f

# Check API manually
curl -X POST http://localhost:8080/v1/memories \
  -H "Content-Type: application/json" \
  -d '{"session":{"user_id":["test"],"session_id":"test"},"producer":"test","produced_for":"bot","episode_content":"test","episode_type":"dialog"}'
```

### Empty Search Results

**Solution**: 
1. Verify data was stored first
2. Try broader queries
3. Check filters aren't too restrictive
4. Wait a moment for indexing

### Enable Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from memmachine_chatbot import MemMachineChatbot
chatbot = MemMachineChatbot(user_id="debug_user")
```

## Add AI-Powered Conversations (Optional)

Want the chatbot to actually respond with AI? Add GPT-4o-mini:

```bash
# Install OpenAI
pip install openai

# Set your API key
export OPENAI_API_KEY='sk-your-key-here'

# Run AI-powered chatbot
python chatbot_with_llm.py
```

**See [GPT4O_MINI_SETUP.md](GPT4O_MINI_SETUP.md) for detailed setup guide!**

## Next Steps

1. ✅ **Read the Full Documentation**: Check out [README.md](README.md) for detailed API reference
2. 🤖 **Add AI Responses**: Use [GPT4O_MINI_SETUP.md](GPT4O_MINI_SETUP.md) to integrate GPT-4o-mini
3. 🎨 **Add a GUI**: Use Streamlit, Gradio, or Flask to create a web interface
4. 🔧 **Customize**: Modify the chatbot for your specific use case
5. 📊 **Analytics**: Add conversation tracking and insights
6. 🌐 **Deploy**: Deploy to production with proper security

## Need Help?

- 📖 **Documentation**: [https://docs.memmachine.ai](https://docs.memmachine.ai)
- 💬 **Discord**: [https://discord.gg/usydANvKqD](https://discord.gg/usydANvKqD)
- 🐛 **Issues**: [GitHub Issues](https://github.com/MemMachine/MemMachine/issues)

## Summary

You now have a working chatbot that can:
- ✅ Store conversations in MemMachine
- ✅ Recall information from past conversations
- ✅ Search through conversation history
- ✅ Manage multiple sessions
- ✅ Be easily integrated into your applications

**That's it! You're ready to build memory-powered chatbots! 🚀**

