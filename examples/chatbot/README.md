# MemMachine Chatbot

A simple, flexible chatbot client for interacting with MemMachine's REST API. This chatbot demonstrates how to store conversations in memory and recall them later.

## Features

- ✅ **Flexible API Configuration**: Configure the MemMachine API URL
- ✅ **Memory Storage**: Store user and assistant messages
- ✅ **Memory Recall**: Search and retrieve past conversations
- ✅ **Session Management**: Manage multiple conversation sessions
- ✅ **Easy to Use**: Simple Python API for integration
- ✅ **Demo Modes**: Both automated demo and interactive chat modes

## Installation

### Prerequisites

1. **MemMachine Backend Running**: Make sure MemMachine is running and accessible
2. **Python 3.8+**: This chatbot requires Python 3.8 or higher
3. **Dependencies**: Install required Python packages

### Install Dependencies

```bash
pip install requests
```

Or if you're using the full MemMachine project:

```bash
# From the project root
pip install -r requirements.txt
```

## Quick Start

### 1. Start MemMachine

Make sure MemMachine is running. If using Docker:

```bash
docker-compose up
```

The API should be available at `http://localhost:8080` by default.

### 2. Run the Demo

```bash
cd examples/chatbot
python demo.py
```

This will run an automated demo that:
- Creates a conversation with multiple turns
- Stores messages in MemMachine
- Recalls specific information (name, profession, interests, etc.)
- Shows session information

### 3. Try Interactive Mode

```bash
python demo.py --interactive
```

This opens an interactive chat where you can:
- Type messages to store them in memory
- Use `/recall <query>` to search memories
- Use `/sessions` to see active sessions
- Use `/quit` to exit

## Usage

### Basic Usage

```python
from memmachine_chatbot import MemMachineChatbot

# Initialize the chatbot
chatbot = MemMachineChatbot(
    base_url="http://localhost:8080",
    user_id="alice",
    agent_id="my_assistant"
)

# Store a user message
chatbot.store_user_message("Hello! My name is Alice.")

# Store an assistant response
chatbot.store_assistant_message("Hi Alice! Nice to meet you.")

# Recall information
result = chatbot.recall("What is the user's name?")
print(result)
```

### Advanced Usage

```python
# Custom memory storage with metadata
chatbot.add_memory(
    content="I love machine learning and Python!",
    producer="alice",
    produced_for="assistant",
    episode_type="dialog",
    metadata={
        "timestamp": "2024-01-15T10:30:00",
        "topic": "interests",
        "sentiment": "positive"
    }
)

# Search with filters
memories = chatbot.search_memory(
    query="interests and hobbies",
    limit=10,
    filter_params={"producer": "alice"}
)

# Get all sessions
sessions = chatbot.get_all_sessions()

# Delete current session
chatbot.delete_session()
```

## Configuration

### Environment Variables

You can configure the chatbot using environment variables:

```bash
export MEMMACHINE_URL="http://localhost:8080"  # MemMachine API URL
export USER_ID="my_user"                       # Default user ID
```

### Python Configuration

```python
chatbot = MemMachineChatbot(
    base_url="http://your-memmachine-server:8080",
    user_id="custom_user",
    session_id="custom_session_123",  # Optional: auto-generated if not provided
    agent_id="custom_assistant"
)
```

## API Reference

### MemMachineChatbot Class

#### `__init__(base_url, user_id, session_id=None, agent_id="chatbot_assistant")`

Initialize a new chatbot instance.

**Parameters:**
- `base_url` (str): MemMachine API URL (default: "http://localhost:8080")
- `user_id` (str): User identifier
- `session_id` (str, optional): Session ID (auto-generated if not provided)
- `agent_id` (str): Agent identifier (default: "chatbot_assistant")

#### `store_user_message(message: str) -> bool`

Store a user message in memory.

**Parameters:**
- `message` (str): The user's message

**Returns:**
- `bool`: True if successful

#### `store_assistant_message(message: str) -> bool`

Store an assistant message in memory.

**Parameters:**
- `message` (str): The assistant's message

**Returns:**
- `bool`: True if successful

#### `recall(query: str) -> str`

Recall memories and format them as a readable string.

**Parameters:**
- `query` (str): What to recall

**Returns:**
- `str`: Formatted string of recalled memories

#### `search_memory(query: str, limit: int = 5, filter_params: dict = None) -> dict`

Search memories in MemMachine.

**Parameters:**
- `query` (str): Search query
- `limit` (int): Maximum results to return (default: 5)
- `filter_params` (dict): Optional filter parameters

**Returns:**
- `dict`: Dictionary with `episodic_memory` and `profile_memory` keys

#### `add_memory(content, producer, produced_for, episode_type="dialog", metadata=None) -> bool`

Add a memory episode with full control over parameters.

**Parameters:**
- `content` (str): Content to store
- `producer` (str): Who produced the content
- `produced_for` (str): Who the content was produced for
- `episode_type` (str): Type of episode (default: "dialog")
- `metadata` (dict): Optional metadata

**Returns:**
- `bool`: True if successful

#### `get_all_sessions() -> List[dict]`

Get all active sessions.

**Returns:**
- `List[dict]`: List of session dictionaries

#### `delete_session() -> bool`

Delete the current session data.

**Returns:**
- `bool`: True if successful

## Demo Modes

### Automated Demo Mode

Runs a pre-programmed conversation demonstrating memory storage and recall:

```bash
python demo.py
```

Output includes:
1. **Phase 1**: Building conversation memory with 4 conversation turns
2. **Phase 2**: Testing memory recall with 5 different queries
3. **Phase 3**: Advanced memory search with filters
4. **Phase 4**: Session information display
5. **Phase 5**: Optional cleanup instructions

### Interactive Mode

Run an interactive chat session:

```bash
python demo.py --interactive
```

Commands in interactive mode:
- Type any message to store it in memory
- `/recall <query>` - Search for memories matching the query
- `/sessions` - List all active sessions
- `/quit` - Exit the interactive session

## Examples

### Example 1: Simple Conversation

```python
from memmachine_chatbot import MemMachineChatbot

chatbot = MemMachineChatbot(user_id="john")

# Simulate a conversation
chatbot.store_user_message("Hi! I'm learning Python.")
chatbot.store_assistant_message("That's great! Python is a versatile language.")
chatbot.store_user_message("I'm particularly interested in machine learning.")
chatbot.store_assistant_message("ML with Python is exciting! Check out scikit-learn and TensorFlow.")

# Recall what the user is learning
result = chatbot.recall("What is the user learning?")
print(result)
```

### Example 2: Multiple Sessions

```python
# Session 1: Morning conversation
morning_chat = MemMachineChatbot(
    user_id="alice",
    session_id="morning_session"
)
morning_chat.store_user_message("Good morning! I need to finish my report today.")

# Session 2: Afternoon conversation
afternoon_chat = MemMachineChatbot(
    user_id="alice",
    session_id="afternoon_session"
)
afternoon_chat.store_user_message("I've completed the report!")

# Both sessions are stored separately
sessions = morning_chat.get_all_sessions()
print(f"Alice has {len([s for s in sessions if 'alice' in s.get('user_ids', [])])} sessions")
```

### Example 3: Custom Metadata

```python
chatbot = MemMachineChatbot(user_id="bob")

# Store with custom metadata
chatbot.add_memory(
    content="Meeting scheduled for Friday at 2 PM",
    producer="bob",
    produced_for="assistant",
    episode_type="reminder",
    metadata={
        "type": "calendar_event",
        "date": "2024-01-19",
        "time": "14:00",
        "priority": "high"
    }
)

# Search for reminders
memories = chatbot.search_memory(
    query="upcoming meetings",
    filter_params={"episode_type": "reminder"}
)
```

## Integration with Other Systems

### Using with LangChain

```python
from memmachine_chatbot import MemMachineChatbot
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage

chatbot = MemMachineChatbot(user_id="user123")
llm = ChatOpenAI()

def chat_with_memory(user_message):
    # Recall relevant context
    context = chatbot.recall(user_message)
    
    # Create prompt with context
    messages = [
        HumanMessage(content=f"Context: {context}\n\nUser: {user_message}")
    ]
    
    # Get LLM response
    response = llm(messages)
    
    # Store in memory
    chatbot.store_user_message(user_message)
    chatbot.store_assistant_message(response.content)
    
    return response.content
```

### Using with Custom Agents

```python
class MyCustomAgent:
    def __init__(self, user_id):
        self.chatbot = MemMachineChatbot(
            base_url="http://localhost:8080",
            user_id=user_id,
            agent_id="custom_agent"
        )
    
    def process_message(self, message):
        # Store incoming message
        self.chatbot.store_user_message(message)
        
        # Get relevant memories
        memories = self.chatbot.search_memory(message, limit=5)
        
        # Process with your custom logic
        response = self.generate_response(message, memories)
        
        # Store response
        self.chatbot.store_assistant_message(response)
        
        return response
    
    def generate_response(self, message, memories):
        # Your custom response generation logic here
        return f"Processed: {message}"
```

## Troubleshooting

### Connection Issues

**Problem**: Cannot connect to MemMachine API

**Solutions**:
1. Verify MemMachine is running: `curl http://localhost:8080/v1/health`
2. Check the URL in your configuration
3. Verify firewall settings aren't blocking the connection
4. Check Docker logs if using Docker: `docker-compose logs`

### Memory Not Storing

**Problem**: Messages aren't being saved

**Solutions**:
1. Check the API response status codes in the logs
2. Verify your session data is correctly formatted
3. Ensure MemMachine has sufficient storage space
4. Check MemMachine logs for errors

### No Memories Returned

**Problem**: Searches return empty results

**Solutions**:
1. Verify memories were stored successfully first
2. Try broader search queries
3. Check if filters are too restrictive
4. Give the system a moment after storing to index the data

### Enable Debug Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)

chatbot = MemMachineChatbot(user_id="debug_user")
```

## Architecture

```
┌─────────────────────┐
│   Your Application  │
│   (demo.py, etc.)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────┐
│  MemMachineChatbot      │
│  - store_user_message() │
│  - store_assistant_...  │
│  - recall()             │
│  - search_memory()      │
└──────────┬──────────────┘
           │
           ▼ HTTP REST API
┌─────────────────────────┐
│   MemMachine API        │
│   (localhost:8080)      │
│                         │
│   /v1/memories (POST)   │
│   /v1/memories/search   │
│   /v1/sessions (GET)    │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│   Storage Layer         │
│   - Graph Database      │
│   - SQL Database        │
└─────────────────────────┘
```

## Contributing

Contributions are welcome! To add features or fix bugs:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with `demo.py`
5. Submit a pull request

## License

This project is part of MemMachine and is licensed under the Apache 2.0 License.

## Support

- **Documentation**: [https://docs.memmachine.ai](https://docs.memmachine.ai)
- **Discord**: [https://discord.gg/usydANvKqD](https://discord.gg/usydANvKqD)
- **Issues**: [GitHub Issues](https://github.com/MemMachine/MemMachine/issues)

## What's Next?

Now that you have the basic chatbot working, you can:

1. **Add GUI**: Create a web interface using Streamlit or Flask
2. **Integrate LLM**: Connect to OpenAI, Anthropic, or other LLM providers
3. **Add Voice**: Implement speech-to-text and text-to-speech
4. **Multi-modal**: Add support for images and documents
5. **Analytics**: Add conversation analytics and insights
6. **Personalization**: Build user profiles based on conversation history

Check out the other examples in the `examples/` directory for more ideas!

