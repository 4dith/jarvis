import requests

API_URL = "https://apifreellm.com/api/chat"

def ask_bot(user_input, history):
    context = "You are a helpful college club help desk assistant.\n"
    for msg in history:
        context += f"{msg['role']}: {msg['content']}\n"
    context += f"User: {user_input}"

    response = requests.post(API_URL, json={"message": context})
    data = response.json()

    if data.get("status") == "success":
        return data["response"]
    else:
        print("Error:", data.get("error"))
        return None

chat_history = []

print("HelpDesk Bot (type 'exit' to quit)")
while True:
    user = input("You: ")
    if user.lower() == "exit":
        break
    reply = ask_bot(user, chat_history)
    if reply:
        print("Bot:", reply)
        chat_history.append({"role": "user", "content": user})
        chat_history.append({"role": "assistant", "content": reply})
