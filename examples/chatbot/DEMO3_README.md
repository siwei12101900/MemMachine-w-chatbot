# Demo 3: Full Memory - Episodic + Profile

Uses the **combined `/v1/memories` endpoint** to leverage both episodic AND profile memory.

## ⚠️ IMPORTANT: Known Bug

**This demo currently triggers a bug in MemMachine's profile memory!**

**Symptoms**:
- HTTP 500 errors when storing memories
- Error: `AttributeError: 'tuple' object has no attribute 'removeprefix'`
- Very slow response times (15-20 seconds)

**✅ Solution**: Use **demo2.py** instead, which uses episodic-only endpoints and works perfectly.

See [PROFILE_MEMORY_BUG.md](PROFILE_MEMORY_BUG.md) for full details and workarounds.

## Key Difference from Demo 2

| Feature | Demo 2 | Demo 3 |
|---------|--------|--------|
| **Endpoint** | `/v1/memories/episodic` | `/v1/memories` |
| **Memory Types** | Episodic only | Episodic + Profile |
| **Fact Extraction** | ❌ No | ✅ Yes |
| **Long-term Facts** | ❌ Not stored | ✅ Automatically extracted |
| **Use Case** | Conversation context | Persistent user profiles |

## What is Profile Memory?

**Profile Memory** automatically extracts and stores long-term facts about users:

- **Name**: "Sarah"
- **Profession**: "Data Engineer"
- **Skills**: "Python", "Neural Networks"
- **Preferences**: "Jazz music", "Paris"
- **Projects**: "Music recommendation system"

These facts persist **across sessions** and are automatically maintained by MemMachine!

## Architecture

```
User Input → "My name is Sarah and I'm a data engineer"
    ↓
┌─────────────────────────────────────────────────────┐
│ POST /v1/memories                                   │
│   MemMachine stores in TWO places:                  │
│   1. Episodic Memory (conversation context)         │
│   2. Profile Memory (extracts "name: Sarah",        │
│                      "job: Data Engineer")          │
└─────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────┐
│ POST /v1/memories/search                            │
│   Returns BOTH:                                     │
│   - episodic_memory: Recent conversation            │
│   - profile_memory: Long-term facts                 │
└─────────────────────────────────────────────────────┘
    ↓
LLM uses BOTH memory types for richer context
```

## Quick Start

```bash
cd examples/chatbot

# Install dependencies
pip install requests openai

# Set API key
export OPENAI_API_KEY='sk-your-key-here'

# Run demo 3
python demo3.py
```

## Sample Output

```
======================================================================
 MemMachine Demo 3: Full Memory (Episodic + Profile)
======================================================================

Architecture: Using /v1/memories for BOTH memory types

┌─────────────────────────────────────────────────────────────┐
│  Episodic Memory → Conversation context & recent events    │
│  Profile Memory  → Long-term facts about user              │
│  Combined API    → Automatic fact extraction               │
└─────────────────────────────────────────────────────────────┘

✓ OpenAI API key found
✓ Using model: gpt-4o-mini
✓ MemMachine connected
✓ Session: session_sarah_20250930_163000
✓ Using: /v1/memories (episodic + profile)

──────────────────────────────────────────────────────────
💬 Turn 1/6: Sarah introduces herself (fact extraction expected)
──────────────────────────────────────────────────────────

👤 Sarah: Hi! My name is Sarah and I'm a data engineer

   📥 [MemMachine] Storing in episodic + profile memory...
      REST API: POST http://localhost:8080/v1/memories
      Response: 200
      ⏱️  Time: 0.342s

   🔍 [MemMachine] Searching episodic + profile memory...
      REST API: POST http://localhost:8080/v1/memories/search
      Response: 200
      Found: 0 episodic, 0 profile memories
      ⏱️  Time: 0.198s

   🤖 [LLM] Generating response with GPT-4o-mini...
      API: OpenAI Chat Completions
   ✅ [LLM] Response generated successfully
      ⏱️  Time: 1.234s

   💾 [MemMachine] Storing AI response...
      REST API: POST http://localhost:8080/v1/memories
      Response: 200
      ⏱️  Time: 0.287s

   📊 Total Turn Time: 2.061s
      ├─ Store user (E+P): 0.342s (16.6%)
      ├─ Search (E+P):     0.198s (9.6%)
      ├─ LLM generation:   1.234s (59.9%)
      └─ Store AI (E+P):   0.287s (13.9%)

🤖 AI: Hello Sarah! It's great to meet a data engineer!

──────────────────────────────────────────────────────────
💭 Memory Test 4/6: 🔍 Memory test: Should use PROFILE memory for facts
──────────────────────────────────────────────────────────

👤 Sarah: what is my name and what do i do for work

   📥 [MemMachine] Storing in episodic + profile memory...
      REST API: POST http://localhost:8080/v1/memories
      Response: 200
      ⏱️  Time: 0.298s

   🔍 [MemMachine] Searching episodic + profile memory...
      REST API: POST http://localhost:8080/v1/memories/search
      Response: 200
      Found: 3 episodic, 2 profile memories    ← Profile facts extracted!
      ⏱️  Time: 0.234s

   🤖 [LLM] Generating response with GPT-4o-mini...
      API: OpenAI Chat Completions
   ✅ [LLM] Response generated successfully
      ⏱️  Time: 1.456s

🤖 AI (Recalling): Your name is Sarah and you're a data engineer 
working on machine learning projects with Python!
```

## Benefits of Profile Memory

### 1. **Persistent Facts**

Facts extracted in one session are available in **future sessions**:

```python
# Session 1 (Today)
User: "My name is Sarah, I'm a data engineer"
→ Profile stores: {name: "Sarah", job: "Data Engineer"}

# Session 2 (Tomorrow - NEW SESSION)
User: "What do you know about me?"
AI: "You're Sarah, a data engineer!"  ← Remembers from profile!
```

### 2. **Automatic Extraction**

MemMachine automatically identifies and extracts facts:

```
User message: "I love Python and jazz music, I'm from Paris"

Profile Memory extracts:
  - programming_language: Python
  - music_preference: Jazz
  - location: Paris
```

### 3. **Structured Knowledge**

Profile memory stores facts in a structured way, making them easier to query and use.

## When to Use Each Demo

### Use Demo 2 (Episodic Only)

- ✅ When you only need conversation context
- ✅ When you want faster performance
- ✅ When profile memory has bugs (workaround)
- ✅ For temporary conversations

### Use Demo 3 (Episodic + Profile)

- ✅ When you need long-term user knowledge
- ✅ When facts should persist across sessions
- ✅ When building personalized assistants
- ✅ For multi-session applications

## API Endpoints Used

### Demo 2 (Episodic Only)
```
POST /v1/memories/episodic        ← Store
POST /v1/memories/episodic/search ← Search
```

### Demo 3 (Full Memory)
```
POST /v1/memories        ← Store (both types)
POST /v1/memories/search ← Search (both types)
```

## Comparison Example

**Same question, different memories:**

### Demo 2 Response (Episodic only)
```
Query: "What do you know about me?"

Episodic Memory:
- "Hi! My name is Sarah"
- "I'm a data engineer"
- "I work with Python"

Response: "Based on our conversation, your name is Sarah,
you're a data engineer who works with Python."
```

### Demo 3 Response (Episodic + Profile)
```
Query: "What do you know about me?"

Profile Memory:
- name: Sarah
- profession: Data Engineer
- skills: [Python, Neural Networks, ML]
- interests: [Jazz, Paris]
- current_project: Music recommendation system

Episodic Memory:
- Recent conversation context

Response: "You're Sarah, a data engineer specializing in 
machine learning with Python and neural networks. You're 
currently building a music recommendation system. You love 
jazz music and Paris is your favorite city!"
```

## Performance Comparison

### Demo 2 (Episodic Only)
```
Store: ~0.2s (episodic only)
Search: ~0.2s (episodic only)
Total: ~0.4s for memory ops
```

### Demo 3 (Episodic + Profile)
```
Store: ~0.3s (both types, +fact extraction)
Search: ~0.2s (both types)
Total: ~0.5s for memory ops (+25% time)
```

**Trade-off**: Slightly slower but much richer memory!

## Known Issues

⚠️ **Profile Memory Bug**: There's a known bug in MemMachine's profile memory that can cause 500 errors:

```python
AttributeError: 'tuple' object has no attribute 'removeprefix'
```

**If you encounter this:**
1. Check MemMachine logs: `docker logs memmachine-app`
2. Use Demo 2 (episodic-only) as workaround
3. Report issue to MemMachine team

## Testing Profile Memory

After running demo3, check what was stored:

```bash
# Search for profile facts
curl -X POST http://localhost:8080/v1/memories/profile/search \
  -H "Content-Type: application/json" \
  -d '{
    "session": {
      "user_id": ["sarah"],
      "session_id": "session_sarah_...",
      "agent_id": ["demo3_assistant"],
      "group_id": null
    },
    "query": "profession skills",
    "limit": 10
  }'
```

## Summary

**Demo 3 = Full Power of MemMachine**

```
┌────────────────────────────────────────────┐
│  Episodic Memory                           │
│  ✓ Conversation context                    │
│  ✓ Recent interactions                     │
│  ✓ Temporal information                    │
├────────────────────────────────────────────┤
│  Profile Memory                            │
│  ✓ Long-term facts                         │
│  ✓ User attributes                         │
│  ✓ Persistent knowledge                    │
│  ✓ Cross-session memory                    │
├────────────────────────────────────────────┤
│  = Rich, Personalized AI Assistant         │
└────────────────────────────────────────────┘
```

Run `python demo3.py` to experience the full memory capabilities! 🚀

