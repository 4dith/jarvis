import requests

API_URL = "https://apifreellm.com/api/chat"

chat_history = []

print("HelpDesk Bot (type 'exit' to quit)")
while True:
    user = input("You: ")
    if user.lower() == "exit":
        break
    reply = "Bot's reply"
    if reply:
        print("Bot:", reply)
        chat_history.append({"role": "user", "content": user})
        chat_history.append({"role": "assistant", "content": reply})
