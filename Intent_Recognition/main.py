from intent_classifier import classify_intent
from param_extractor import extract_parameters

while True:
    text = input("You: ")
    if text.lower() in ["quit", "exit"]:
        break

    intent, score = classify_intent(text)
    params = extract_parameters(text, intent)
    print(f"Intent: {intent} (score={score:.2f}), Params: {params}")
