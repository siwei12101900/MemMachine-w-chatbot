# Demo 2: Sarah's Journey - Memory-Powered Conversation

An interactive demonstration of MemMachine's memory capabilities with GPT-4o-mini.

## What This Demo Shows

Watch as the AI:
- **Remembers** Sarah's name, profession, and interests
- **Recalls** specific details when asked
- **Maintains context** throughout the conversation
- **Demonstrates** perfect memory across 9 conversation turns

## The Conversation

Sarah (a data engineer) has a conversation with the AI about:
1. Her introduction (name and profession)
2. Her ML project using Python
3. Her recommendation system project
4. **Memory Test**: Recalls name and profession
5. **Memory Test**: Recalls programming language
6. **Memory Test**: Recalls ML interests
7. Her hobbies (hiking, traveling)
8. Her favorite city (Paris)
9. **Final Test**: Comprehensive recall of all information

## Prerequisites

1. **MemMachine running**: `docker ps | grep memmachine`
2. **Python packages**: `pip install requests openai`
3. **OpenAI API key**: Get from https://platform.openai.com/api-keys

## Quick Start

```bash
# 1. Navigate to chatbot directory
cd examples/chatbot

# 2. Install dependencies (if not already installed)
pip install requests openai

# 3. Set your OpenAI API key
export OPENAI_API_KEY='sk-your-actual-key-here'

# 4. Run the demo
python demo2.py
```

## Expected Output

```
======================================================================
 MemMachine Demo 2: Sarah's Journey
======================================================================

Demonstrating memory-powered conversations with GPT-4o-mini
Watch how the AI remembers and recalls information!

✓ OpenAI API key found
✓ Using model: gpt-4o-mini
✓ MemMachine connected
✓ Session: session_sarah_20250930_...

Press Enter to start the conversation...

──────────────────────────────────────────────────────────────────────
💬 Turn 1/9: Sarah introduces herself
──────────────────────────────────────────────────────────────────────

👤 Sarah: Hi! My name is Sarah and I'm a data engineer
   💾 Storing in memory...
   🤔 Thinking...

🤖 AI: Hello Sarah! It's great to meet a data engineer! What kind of 
projects are you working on?

Press Enter to continue...

──────────────────────────────────────────────────────────────────────
💬 Turn 2/9: Sarah shares her work and interests
──────────────────────────────────────────────────────────────────────

👤 Sarah: I'm currently working on a machine learning project using Python. 
I love working with neural networks!
   💾 Storing in memory...
   🤔 Thinking...

🤖 AI: That's fantastic! Neural networks are fascinating. Python is 
perfect for ML work with libraries like TensorFlow and PyTorch. What 
specific problem are you solving with your neural network?

Press Enter to continue...

──────────────────────────────────────────────────────────────────────
💬 Turn 3/9: Sarah describes her project
──────────────────────────────────────────────────────────────────────

👤 Sarah: I'm building a recommendation system for a music streaming app. 
It's quite challenging but exciting!
   💾 Storing in memory...
   🤔 Thinking...

🤖 AI: A music recommendation system sounds like a really exciting project! 
That's a perfect use case for neural networks. Are you using collaborative 
filtering or content-based approaches?

Press Enter to continue...

──────────────────────────────────────────────────────────────────────
💭 Memory Test 4/9: 🔍 Testing memory recall: Name and profession
──────────────────────────────────────────────────────────────────────

👤 Sarah: what is my name and what do i do for work
   💾 Storing in memory...
   🤔 Thinking...

🤖 AI (Recalling): Your name is Sarah and you're a data engineer. You're 
currently working on building a recommendation system for a music streaming 
app using machine learning and neural networks!

Press Enter to continue...

... [continues for all 9 turns] ...

======================================================================
 Demo Complete!
======================================================================

✓ All messages stored in MemMachine
✓ AI successfully recalled:
  - Sarah's name and profession
  - Programming language (Python)
  - ML interest (neural networks)
  - Personal hobbies (hiking, traveling)
  - Favorite city (Paris)
  - Complete professional and personal profile

Session ID: session_sarah_20250930_154530

The AI demonstrated perfect memory recall throughout the conversation!
```

## Key Features Demonstrated

### 1. Information Storage
- Every message is stored in MemMachine's episodic memory
- Metadata includes timestamps and speaker information

### 2. Context-Aware Responses
- AI generates natural, conversational responses
- Responses build on previous context

### 3. Memory Recall
- AI accurately answers questions about past conversation
- Demonstrates both specific and comprehensive recall

### 4. Session Management
- All data stored in a single session
- Can be retrieved later or across conversations

## Comparison with Other Demos

| Demo | Purpose | LLM | Interactive |
|------|---------|-----|-------------|
| `demo.py` | Basic memory test | ❌ No | ✓ Yes |
| `chatbot_with_llm.py` | Interactive chat | ✓ GPT-4o-mini | ✓ Live input |
| **`demo2.py`** | **Scripted showcase** | **✓ GPT-4o-mini** | **✓ Step-through** |

## Customization

### Change the Conversation

Edit the `conversation` list in `demo2.py`:

```python
conversation = [
    {
        "user": "Your custom message here",
        "is_question": False,  # Set to True for memory tests
        "note": "Description of this turn"
    },
    # Add more turns...
]
```

### Change the User

Modify the initialization:

```python
chatbot = MemMachineChatbot(
    user_id="your_name",  # Change user
    agent_id="custom_assistant"  # Change assistant name
)
```

### Change the Model

Modify the OpenAI call:

```python
response = client.chat.completions.create(
    model="gpt-4o",  # or "gpt-3.5-turbo"
    temperature=0.9,  # More creative
    max_tokens=1000   # Longer responses
)
```

## Troubleshooting

### "OPENAI_API_KEY not found"
```bash
export OPENAI_API_KEY='sk-your-key-here'
```

### "Failed to connect to MemMachine"
```bash
# Check if MemMachine is running
docker ps | grep memmachine

# Restart if needed
docker restart memmachine-app
```

### "ModuleNotFoundError: No module named 'requests'"
```bash
pip install requests openai
```

### AI Doesn't Remember
- Check that previous messages completed successfully
- Look for any error messages in the output
- Verify MemMachine health: `curl http://localhost:8080/health`

## Cost Estimate

For this 9-turn conversation:
- Approximately 2,000-3,000 tokens total
- Cost: **~$0.001** (less than a penny!)

GPT-4o-mini is very affordable for development and testing.

## Next Steps

1. **Run the demo**: `python demo2.py`
2. **Modify the conversation**: Add your own turns
3. **Build your own**: Use as a template for your application
4. **Try other models**: Test GPT-4o or GPT-3.5-turbo
5. **Add GUI**: Create a web interface with Streamlit

## Files in This Project

- **demo2.py** - This interactive demo
- **demo.py** - Basic demo without LLM
- **chatbot_with_llm.py** - Interactive freeform chat
- **memmachine_chatbot.py** - Core chatbot client library

## Summary

Demo 2 is a perfect showcase of MemMachine's memory capabilities:
- ✓ Stores all conversation context
- ✓ Enables accurate memory recall
- ✓ Powers intelligent, context-aware AI responses
- ✓ Easy to customize and extend

**Ready to see it in action?**

```bash
python demo2.py
```

Enjoy! 🚀

