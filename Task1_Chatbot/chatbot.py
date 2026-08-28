print("🤖 Rule-Based Chatbot")
print("Type 'bye' to exit.\n")

while True:
    user_input = input("You: ").lower().strip()

    if user_input in ["hello", "hi", "hey"]:
        print("Bot: Hello! How can I help you?")

    elif "how are you" in user_input:
        print("Bot: I'm doing great! Thanks for asking.")

    elif "your name" in user_input:
        print("Bot: I am a Rule-Based AI Chatbot.")

    elif "help" in user_input:
        print("Bot: I can respond to greetings, questions about myself, and simple conversations.")

    elif user_input in ["bye", "goodbye", "exit"]:
        print("Bot: Goodbye! Have a nice day.")
        break

    else:
        print("Bot: Sorry, I don't understand that yet.")