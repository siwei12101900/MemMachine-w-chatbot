# GPT-4o-mini Setup Guide

Quick guide to get started with GPT-4o-mini integration in your MemMachine chatbot.

## What is GPT-4o-mini?

GPT-4o-mini is OpenAI's fast and affordable small model:
- ✅ **Fast**: Quick response times
- ✅ **Affordable**: ~15x cheaper than GPT-4
- ✅ **Capable**: Great for most chatbot tasks
- ✅ **Smart**: Good reasoning and context understanding

**Cost**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens

## Quick Start (3 Steps)

### Step 1: Install OpenAI Package

```bash
cd examples/chatbot
pip install openai
```

Or install from requirements:
```bash
pip install -r requirements.txt
```

### Step 2: Get Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in (or create an account)
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. **Save it somewhere safe!** (you won't see it again)

### Step 3: Set Your API Key

```bash
export OPENAI_API_KEY='sk-your-actual-key-here'
```

**That's it!** Now run the chatbot:

```bash
python chatbot_with_llm.py
```

## Usage Example

```bash
$ python chatbot_with_llm.py

======================================================================
 MemMachine Chatbot with GPT-4o-mini
======================================================================

✓ OpenAI API key found
✓ Using model: gpt-4o-mini
✓ MemMachine connected
✓ Session: session_llm_user_20240130_150000

Ready to chat! The AI has access to conversation memory.

Commands:
  - Type a message to chat with GPT-4o-mini
  - Type '/quit' to exit

======================================================================

You: Hi! My name is Alice and I'm a software engineer.
  💾 Stored in memory...
  🤔 Thinking...

AI: Hello Alice! It's great to meet you! What kind of software engineering 
do you specialize in? Are there any projects you're currently working on?

You: I love Python and machine learning!
  💾 Stored in memory...
  🤔 Thinking...

AI: That's fantastic! Python is a great language for machine learning. Are 
you working with any specific ML frameworks like TensorFlow, PyTorch, or 
scikit-learn? I'd love to hear about what you're building!

You: What's my name?
  💾 Stored in memory...
  🤔 Thinking...

AI: Your name is Alice! You mentioned earlier that you're a software engineer
who loves Python and machine learning.

You: /quit
Goodbye!
```

Notice how the AI **remembers** your name and interests from earlier in the conversation!

## Full Example with Code

Create a file called `test_gpt4o.py`:

```python
import os
from openai import OpenAI
from memmachine_chatbot import MemMachineChatbot

# Set your API key
os.environ["OPENAI_API_KEY"] = "sk-your-key-here"

# Initialize
client = OpenAI()
chatbot = MemMachineChatbot(user_id="alice")

# First message
user_msg = "Hi! I'm Alice, a Python developer."
chatbot.store_user_message(user_msg)

# Get AI response with memory context
context = chatbot.recall(user_msg)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"Context: {context}"},
        {"role": "user", "content": user_msg}
    ]
)

ai_msg = response.choices[0].message.content
chatbot.store_assistant_message(ai_msg)
print(f"AI: {ai_msg}")

# Second message - AI will remember!
user_msg2 = "What's my name and job?"
chatbot.store_user_message(user_msg2)

context = chatbot.recall(user_msg2)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"Context: {context}"},
        {"role": "user", "content": user_msg2}
    ]
)

ai_msg2 = response.choices[0].message.content
chatbot.store_assistant_message(ai_msg2)
print(f"AI: {ai_msg2}")  # Will remember Alice is a Python developer!
```

Run it:
```bash
python test_gpt4o.py
```

## Configuration Options

### Model Selection

You can easily switch models in `chatbot_with_llm.py`:

```python
# Edit line 59 in chatbot_with_llm.py
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Change this to:
    # model="gpt-4o",           # More capable, more expensive
    # model="gpt-4-turbo",      # Previous generation
    # model="gpt-3.5-turbo",    # Cheaper, faster
    messages=messages,
    temperature=0.7,      # Creativity (0.0-2.0)
    max_tokens=500        # Max response length
)
```

### Temperature Setting

```python
temperature=0.7   # Default: balanced
temperature=0.3   # More focused, deterministic
temperature=1.0   # More creative, varied
```

### Token Limits

```python
max_tokens=500    # Default: ~500 words
max_tokens=1000   # Longer responses
max_tokens=100    # Shorter, concise responses
```

## Environment Variables

Set these to customize:

```bash
# Required
export OPENAI_API_KEY='sk-your-key'

# Optional
export MEMMACHINE_URL='http://localhost:8080'    # MemMachine API URL
export USER_ID='your_user_id'                    # Your user identifier
```

## Cost Estimation

GPT-4o-mini pricing (as of 2024):
- Input: ~$0.15 per 1M tokens
- Output: ~$0.60 per 1M tokens

**Example conversation cost:**
- 10 message exchange
- ~200 tokens per message
- ~2,000 total tokens
- **Cost: ~$0.001** (less than a penny!)

Compare to GPT-4:
- Same conversation: ~$0.06 (60x more expensive)

## Troubleshooting

### "OpenAI package not installed"

```bash
pip install openai
```

### "OPENAI_API_KEY not found"

```bash
# Set it in your shell
export OPENAI_API_KEY='sk-your-key-here'

# Or add to ~/.bashrc or ~/.zshrc for persistence
echo "export OPENAI_API_KEY='sk-your-key-here'" >> ~/.zshrc
source ~/.zshrc
```

### "Failed to connect to MemMachine"

Make sure MemMachine is running:
```bash
# Check health
curl http://localhost:8080/v1/health

# Start if needed
docker-compose up
```

### "Rate limit exceeded"

If you see rate limit errors:
1. Wait a few minutes
2. Check your OpenAI usage limits at https://platform.openai.com/usage
3. Consider upgrading your OpenAI plan

### "Insufficient credits"

Add credits to your OpenAI account:
1. Go to https://platform.openai.com/account/billing
2. Add payment method
3. Add credits ($5 minimum)

## Testing the Integration

Quick test without running the full chatbot:

```bash
# Test OpenAI connection
python -c "from openai import OpenAI; client = OpenAI(); print('✓ OpenAI connected')"

# Test MemMachine connection
curl http://localhost:8080/v1/health

# Test both together
python chatbot_with_llm.py
```

## Features

The chatbot with GPT-4o-mini integration provides:

✅ **Memory-Enhanced Conversations**
- AI remembers previous messages
- Recalls user preferences and facts
- Provides personalized responses

✅ **Natural Language Understanding**
- Understands context and nuance
- Handles complex queries
- Generates human-like responses

✅ **Fast & Affordable**
- Quick response times
- Low cost per conversation
- Suitable for production use

✅ **Easy Integration**
- Simple Python API
- Works with existing MemMachine setup
- Easy to customize

## Advanced Usage

### Custom System Prompt

Modify the system prompt in `chatbot_with_llm.py`:

```python
messages = [
    {
        "role": "system", 
        "content": "You are a friendly Python expert assistant..."  # Customize!
    }
]
```

### Multiple Models

Run different models for different tasks:

```python
# For complex questions: GPT-4o
complex_response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...]
)

# For simple questions: GPT-4o-mini
simple_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...]
)
```

### Streaming Responses

For real-time streaming:

```python
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## Next Steps

1. ✅ **Test it out**: Run `python chatbot_with_llm.py`
2. 🎨 **Customize**: Modify the system prompt for your use case
3. 🔧 **Integrate**: Add to your own application
4. 📊 **Monitor**: Track usage at https://platform.openai.com/usage
5. 🚀 **Deploy**: Move to production with proper error handling

## Model Comparison

| Model | Speed | Cost | Quality | Best For |
|-------|-------|------|---------|----------|
| **gpt-4o-mini** | ⚡⚡⚡ | 💰 | ⭐⭐⭐⭐ | **Most chatbots** |
| gpt-4o | ⚡⚡ | 💰💰💰 | ⭐⭐⭐⭐⭐ | Complex reasoning |
| gpt-3.5-turbo | ⚡⚡⚡⚡ | 💰 | ⭐⭐⭐ | Simple tasks |

**Recommendation**: Start with **gpt-4o-mini** - it's the sweet spot for most use cases!

## Resources

- **OpenAI API Docs**: https://platform.openai.com/docs
- **Pricing**: https://openai.com/pricing
- **Usage Dashboard**: https://platform.openai.com/usage
- **API Keys**: https://platform.openai.com/api-keys
- **MemMachine Docs**: https://docs.memmachine.ai

## Summary

```
┌────────────────────────────────────────────────────┐
│ ✅ Setup Complete!                                 │
├────────────────────────────────────────────────────┤
│ 1. Install: pip install openai                    │
│ 2. Get key: platform.openai.com/api-keys          │
│ 3. Set key: export OPENAI_API_KEY='sk-...'        │
│ 4. Run: python chatbot_with_llm.py                │
└────────────────────────────────────────────────────┘

Now you have a memory-powered AI chatbot! 🚀
```

Questions? Check the [main README](README.md) or [MemMachine docs](https://docs.memmachine.ai).

