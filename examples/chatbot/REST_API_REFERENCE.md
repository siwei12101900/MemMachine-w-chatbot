# MemMachine REST API Reference

Complete documentation of the REST API endpoints used by the chatbot.

## Endpoints Used

### 1. Store Memory (Episodic)
**Endpoint**: `POST /v1/memories/episodic`

**Purpose**: Store a message in episodic memory

**Request**:
```http
POST http://localhost:8080/v1/memories/episodic
Content-Type: application/json

{
  "session": {
    "user_id": ["sarah"],
    "session_id": "session_sarah_20250930_160000",
    "agent_id": ["demo2_assistant"],
    "group_id": null
  },
  "producer": "sarah",
  "produced_for": "demo2_assistant",
  "episode_content": "Hi! My name is Sarah and I'm a data engineer",
  "episode_type": "dialog",
  "metadata": {
    "timestamp": "2025-09-30T16:00:00",
    "speaker": "user",
    "type": "user_message"
  }
}
```

**Response**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

null
```

**Used By**:
- `chatbot.store_user_message()` - Store user messages
- `chatbot.store_assistant_message()` - Store AI responses

---

### 2. Search Memory (Episodic)
**Endpoint**: `POST /v1/memories/episodic/search`

**Purpose**: Search and retrieve relevant memories

**Request**:
```http
POST http://localhost:8080/v1/memories/episodic/search
Content-Type: application/json

{
  "session": {
    "user_id": ["sarah"],
    "session_id": "session_sarah_20250930_160000",
    "agent_id": ["demo2_assistant"],
    "group_id": null
  },
  "query": "what is my name",
  "limit": 5,
  "filter": null
}
```

**Response**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": 0,
  "content": {
    "episodic_memory": [
      [
        {
          "uuid": "abc-123-def",
          "episode_type": "dialog",
          "content_type": "string",
          "content": "Hi! My name is Sarah and I'm a data engineer",
          "timestamp": "2025-09-30T16:00:00",
          "group_id": "demo2_assistant",
          "session_id": "session_sarah_20250930_160000",
          "producer_id": "sarah",
          "produced_for_id": "demo2_assistant",
          "user_metadata": {
            "timestamp": "2025-09-30T16:00:00",
            "speaker": "user",
            "type": "user_message"
          }
        }
      ]
    ]
  }
}
```

**Used By**:
- `chatbot.search_memory()` - Search for relevant context
- `chatbot.recall()` - Format and return memories

---

### 3. Health Check
**Endpoint**: `GET /health`

**Purpose**: Verify MemMachine is running

**Request**:
```http
GET http://localhost:8080/health
```

**Response**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "healthy",
  "service": "memmachine",
  "version": "1.0.0",
  "memory_managers": {
    "profile_memory": true,
    "episodic_memory": true
  }
}
```

**Used By**:
- `chatbot._check_health()` - Connection verification

---

## Demo Output with REST API Details

When you run `demo2.py`, you'll see:

```
──────────────────────────────────────────────────────────
💬 Turn 1/9: Sarah introduces herself
──────────────────────────────────────────────────────────

👤 Sarah: Hi! My name is Sarah and I'm a data engineer

   📥 [MemMachine] Storing message in memory...
      REST API: POST http://localhost:8080/v1/memories/episodic
2025-09-30 16:00:00,123 - memmachine_chatbot - INFO - HTTP POST http://localhost:8080/v1/memories/episodic
2025-09-30 16:00:00,125 - memmachine_chatbot - INFO -   Payload: producer=sarah, content=Hi! My name is Sarah and I'm a data engin...
2025-09-30 16:00:00,234 - memmachine_chatbot - INFO -   Response: 200 OK

   🔍 [MemMachine] Retrieving relevant memories...
      REST API: POST http://localhost:8080/v1/memories/episodic/search
2025-09-30 16:00:00,345 - memmachine_chatbot - INFO - HTTP POST http://localhost:8080/v1/memories/episodic/search
2025-09-30 16:00:00,347 - memmachine_chatbot - INFO -   Query: 'Hi! My name is Sarah and I'm a data engineer', Limit: 5
2025-09-30 16:00:00,456 - memmachine_chatbot - INFO -   Response: 200 OK
2025-09-30 16:00:00,458 - memmachine_chatbot - INFO -   Found: 0 memories
   📚 [MemMachine] Found 0 memory entries

   🤖 [LLM] Generating response with GPT-4o-mini...
   ✅ [LLM] Response generated successfully

   💾 [MemMachine] Storing AI response...
      REST API: POST http://localhost:8080/v1/memories/episodic
2025-09-30 16:00:03,567 - memmachine_chatbot - INFO - HTTP POST http://localhost:8080/v1/memories/episodic
2025-09-30 16:00:03,569 - memmachine_chatbot - INFO -   Payload: producer=demo2_assistant, content=Hello Sarah! It's great to meet a data en...
2025-09-30 16:00:03,678 - memmachine_chatbot - INFO -   Response: 200 OK

🤖 AI: Hello Sarah! It's great to meet a data engineer!
```

## REST API Call Sequence

For each conversation turn:

```
1. User sends message
   ↓
2. POST /v1/memories/episodic (store user message)
   ↓
3. POST /v1/memories/episodic/search (retrieve context)
   ↓
4. LLM generates response (not a REST call)
   ↓
5. POST /v1/memories/episodic (store AI response)
   ↓
6. Display to user
```

## Request/Response Details

### Storing a Message

**What chatbot does**:
```python
chatbot.store_user_message("Hi! My name is Sarah", verbose=True)
```

**HTTP Request**:
```
POST /v1/memories/episodic
Host: localhost:8080
Content-Type: application/json
Content-Length: 412

{
  "session": { ... },
  "producer": "sarah",
  "produced_for": "demo2_assistant",
  "episode_content": "Hi! My name is Sarah",
  "episode_type": "dialog",
  "metadata": { ... }
}
```

**HTTP Response**:
```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 4

null
```

### Searching Memory

**What chatbot does**:
```python
memories = chatbot.search_memory("name", limit=5, verbose=True)
```

**HTTP Request**:
```
POST /v1/memories/episodic/search
Host: localhost:8080
Content-Type: application/json

{
  "session": { ... },
  "query": "name",
  "limit": 5,
  "filter": null
}
```

**HTTP Response**:
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": 0,
  "content": {
    "episodic_memory": [
      [ { "content": "Hi! My name is Sarah", ... } ]
    ]
  }
}
```

## Testing REST APIs Manually

### Using curl

```bash
# 1. Store a memory
curl -X POST http://localhost:8080/v1/memories/episodic \
  -H "Content-Type: application/json" \
  -d '{
    "session": {
      "user_id": ["test"],
      "session_id": "test_session",
      "agent_id": ["bot"],
      "group_id": null
    },
    "producer": "test",
    "produced_for": "bot",
    "episode_content": "Hello world",
    "episode_type": "dialog",
    "metadata": {"timestamp": "2025-09-30T16:00:00"}
  }'

# 2. Search memories
curl -X POST http://localhost:8080/v1/memories/episodic/search \
  -H "Content-Type: application/json" \
  -d '{
    "session": {
      "user_id": ["test"],
      "session_id": "test_session",
      "agent_id": ["bot"],
      "group_id": null
    },
    "query": "hello",
    "limit": 5
  }'
```

### Using Python requests

```python
import requests

base_url = "http://localhost:8080"

# Store memory
store_response = requests.post(
    f"{base_url}/v1/memories/episodic",
    json={
        "session": {
            "user_id": ["test"],
            "session_id": "test_session",
            "agent_id": ["bot"],
            "group_id": None
        },
        "producer": "test",
        "produced_for": "bot",
        "episode_content": "Hello world",
        "episode_type": "dialog",
        "metadata": {"timestamp": "2025-09-30T16:00:00"}
    }
)
print(f"Store: {store_response.status_code}")

# Search memories
search_response = requests.post(
    f"{base_url}/v1/memories/episodic/search",
    json={
        "session": {
            "user_id": ["test"],
            "session_id": "test_session",
            "agent_id": ["bot"],
            "group_id": None
        },
        "query": "hello",
        "limit": 5
    }
)
print(f"Search: {search_response.status_code}")
print(f"Results: {search_response.json()}")
```

## Error Responses

### 500 Internal Server Error

**Cause**: MemMachine configuration issue

**Example**:
```json
{
  "detail": "Internal Server Error"
}
```

**Solutions**: See TROUBLESHOOTING.md

### 404 Not Found

**Cause**: Wrong endpoint URL

**Example**:
```json
{
  "detail": "Not Found"
}
```

**Solution**: Check endpoint spelling and version (`/v1/memories/episodic`)

## Summary

The chatbot uses **2 main REST APIs**:

1. **POST /v1/memories/episodic** - Store messages (3x per turn)
   - Store user message
   - Store AI response
   
2. **POST /v1/memories/episodic/search** - Retrieve context (1x per turn)
   - Search for relevant memories

**Total API calls per conversation turn**: 3 calls
- 1 store (user message)
- 1 search (retrieve context)
- 1 store (AI response)

Run `python demo2.py` to see all these REST API calls in action!

