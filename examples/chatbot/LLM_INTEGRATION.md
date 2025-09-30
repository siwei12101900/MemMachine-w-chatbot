# Adding LLM Integration (Optional)

## Do I Need an OpenAI API Key?

**For the basic chatbot (`demo.py`)**: **NO** ❌  
- The basic chatbot only handles memory storage/retrieval
- No AI-generated responses
- No API key needed

**For AI-powered conversations**: **YES** ✅  
- If you want the chatbot to generate intelligent responses
- If you want actual conversation with an AI
- You'll need an API key from OpenAI, Anthropic, or another provider

## Summary

```
┌─────────────────────────────────────────────────────────┐
│ Current Chatbot (demo.py)                               │
│ ✅ Memory storage         → No API key needed           │
│ ✅ Memory retrieval       → No API key needed           │
│ ✅ Session management     → No API key needed           │
│ ❌ AI responses           → Not included                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ With LLM Integration (chatbot_with_llm.py)              │
│ ✅ Memory storage         → No API key needed           │
│ ✅ Memory retrieval       → No API key needed           │
│ ✅ Session management     → No API key needed           │
│ ✅ AI responses           → API key REQUIRED            │
└─────────────────────────────────────────────────────────┘
```

## Adding OpenAI Integration

### Step 1: Get an API Key

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new secret key
5. Copy the key (you won't see it again!)

### Step 2: Install OpenAI Package

```bash
pip install openai
```

Or for LangChain:
```bash
pip install langchain openai
```

### Step 3: Set Your API Key

**Option A: Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY='sk-...'
```

**Option B: In Code (Not Recommended for Production)**
```python
import openai
openai.api_key = "sk-..."
```

### Step 4: Run the LLM-Powered Chatbot

```bash
python chatbot_with_llm.py
```

## Example: Simple OpenAI Integration

Create a file called `my_ai_chatbot.py`:

```python
import os
import openai
from memmachine_chatbot import MemMachineChatbot

# Set your API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize MemMachine chatbot
chatbot = MemMachineChatbot(user_id="alice")

def chat(user_message):
    # Store user message in memory
    chatbot.store_user_message(user_message)
    
    # Get relevant context from memory
    context = chatbot.recall(user_message)
    
    # Generate AI response with context
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system", 
                "content": f"You are a helpful assistant. Here's what you remember:\n{context}"
            },
            {"role": "user", "content": user_message}
        ]
    )
    
    ai_message = response.choices[0].message.content
    
    # Store AI response in memory
    chatbot.store_assistant_message(ai_message)
    
    return ai_message

# Use it
print(chat("Hi! My name is Alice and I love Python."))
print(chat("What's my name?"))  # AI will remember from memory!
```

Run it:
```bash
export OPENAI_API_KEY='sk-...'
python my_ai_chatbot.py
```

## Example: LangChain Integration

```python
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from memmachine_chatbot import MemMachineChatbot

# Initialize
llm = ChatOpenAI(
    model="gpt-4",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

chatbot = MemMachineChatbot(user_id="bob")

def chat_with_memory(user_message):
    # Store in memory
    chatbot.store_user_message(user_message)
    
    # Get context
    context = chatbot.recall(user_message)
    
    # Create messages with context
    messages = [
        SystemMessage(content=f"Context from previous conversations:\n{context}"),
        HumanMessage(content=user_message)
    ]
    
    # Get AI response
    response = llm(messages)
    
    # Store response
    chatbot.store_assistant_message(response.content)
    
    return response.content

# Test it
print(chat_with_memory("I'm a software engineer working on ML"))
print(chat_with_memory("What do I do for work?"))
```

## Alternative LLM Providers

You don't have to use OpenAI! Here are alternatives:

### Anthropic Claude

```python
import anthropic
from memmachine_chatbot import MemMachineChatbot

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
chatbot = MemMachineChatbot(user_id="user")

def chat(user_message):
    chatbot.store_user_message(user_message)
    context = chatbot.recall(user_message)
    
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        system=f"Context: {context}",
        messages=[{"role": "user", "content": user_message}]
    )
    
    response = message.content[0].text
    chatbot.store_assistant_message(response)
    return response
```

### Local Models (Ollama)

```python
import requests
from memmachine_chatbot import MemMachineChatbot

chatbot = MemMachineChatbot(user_id="user")

def chat(user_message):
    chatbot.store_user_message(user_message)
    context = chatbot.recall(user_message)
    
    # Call local Ollama
    response = requests.post('http://localhost:11434/api/generate', json={
        "model": "llama2",
        "prompt": f"Context: {context}\n\nUser: {user_message}",
        "stream": False
    })
    
    ai_message = response.json()['response']
    chatbot.store_assistant_message(ai_message)
    return ai_message
```

### Hugging Face Models

```python
from transformers import pipeline
from memmachine_chatbot import MemMachineChatbot

generator = pipeline('text-generation', model='gpt2')
chatbot = MemMachineChatbot(user_id="user")

def chat(user_message):
    chatbot.store_user_message(user_message)
    context = chatbot.recall(user_message)
    
    prompt = f"Context: {context}\nUser: {user_message}\nAssistant:"
    response = generator(prompt, max_length=100)[0]['generated_text']
    
    ai_message = response.split("Assistant:")[-1].strip()
    chatbot.store_assistant_message(ai_message)
    return ai_message
```

## Cost Considerations

| Provider | Model | Cost per 1K tokens (input/output) | Free Tier |
|----------|-------|-----------------------------------|-----------|
| OpenAI | GPT-4 | $0.03 / $0.06 | $5 credit for new accounts |
| OpenAI | GPT-3.5 | $0.0015 / $0.002 | $5 credit for new accounts |
| Anthropic | Claude 3 | $0.015 / $0.075 | Limited free tier |
| Local (Ollama) | Llama 2 | **FREE** | Unlimited (runs locally) |
| Hugging Face | Various | **FREE** | Unlimited (runs locally) |

## Testing Without an API Key

You can test the memory functionality without any API key:

```bash
# Run the basic demo (no API key needed)
python demo.py

# Interactive mode (no API key needed)
python demo.py --interactive
```

## Summary

**Current Setup:**
- ✅ **Works now**: Memory storage, retrieval, session management
- ❌ **Not included**: AI-generated responses

**To Add AI Responses:**
1. Get API key from OpenAI or another provider
2. Install the provider's package (`pip install openai`)
3. Set your API key as environment variable
4. Use the `chatbot_with_llm.py` example or create your own

**The chatbot I built is ready to use right now for memory management!**

If you want to add AI later, you can follow this guide. For now, you can test everything with the basic `demo.py` script.

## Need Help?

- OpenAI API Docs: https://platform.openai.com/docs
- LangChain Docs: https://python.langchain.com/
- Anthropic Docs: https://docs.anthropic.com/
- Ollama (Local): https://ollama.ai/

## Quick Decision Tree

```
Do you want AI-generated responses?
│
├─ NO → Use demo.py (no API key needed) ✅
│
└─ YES → Do you want to pay for API calls?
    │
    ├─ YES → Use OpenAI/Anthropic (best quality)
    │         Get API key → Set OPENAI_API_KEY → Run chatbot_with_llm.py
    │
    └─ NO → Use local models (Ollama/Hugging Face)
              Install Ollama → Free, runs on your computer
```

**Bottom line**: The chatbot works perfectly right now without any API key! You only need one if you want to add AI-powered conversation later. 🚀

