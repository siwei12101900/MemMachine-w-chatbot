from memmachine_chatbot import MemMachineChatbot

print("Testing MemMachine connection...")
chatbot = MemMachineChatbot(user_id="charlie")

print("\nStoring message...")
success = chatbot.store_user_message("Hi, my name is Charlie and I am a data engineer")
print(f"  Result: {'✓ Success' if success else '✗ Failed'}")

print("\nRecalling information...")
result = chatbot.recall("What is my name?")
print(f"  Result: {result[:100] if result else 'No results'}...")

print("\n✓ Test complete!")
