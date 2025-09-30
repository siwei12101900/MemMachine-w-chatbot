#!/usr/bin/env python3
"""Quick test of the fixed chatbot"""

import sys
sys.path.insert(0, '/Users/charlieyu/Dropbox/MemVerge/Software/GitHub/MemMachine/examples/chatbot')

from memmachine_chatbot import MemMachineChatbot

print("=" * 70)
print(" Testing Fixed MemMachine Chatbot")
print("=" * 70)
print()

# Initialize
print("1. Initializing chatbot...")
chatbot = MemMachineChatbot(user_id="charlie_test", session_id="test_session_final")
print("   ✓ Connected!\n")

# Store a message
print("2. Storing message: 'My name is Charlie and I am a data engineer'")
success = chatbot.store_user_message("My name is Charlie and I am a data engineer")
print(f"   {'✓ Stored!' if success else '✗ Failed'}\n")

# Recall
print("3. Recalling: 'What is my name?'")
result = chatbot.recall("What is my name?")
print(f"   Result:\n{result}\n")

print("=" * 70)
print(" Test Complete!")
print("=" * 70)

