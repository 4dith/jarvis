import requests

API_URL = "https://apifreellm.com/api/chat"

with open("chatbot_module/context.txt", "r") as f:
    context = f.read()

def ask_bot(user_input):
    global file_text
    message = "You are a helpful college club help desk assistant.\nContext:\n" + context + "\nUser Question: " + user_input

    response = requests.post(API_URL, json={"message": message})
    data = response.json()

    if data.get("status") == "success":
        return data["response"]
    else:
        print("Error:", data.get("error"))
        return None

print("HelpDesk Bot (type 'exit' to quit)")

while True:
    user = input("You: ")
    if user.lower() == "exit":
        break
    reply = ask_bot(user)
    if reply:
        print("\nBot:", reply + "\n")