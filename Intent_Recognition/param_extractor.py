import re
import spacy
nlp = spacy.load("en_core_web_sm")

def extract_parameters(user_input, intent):
    doc = nlp(user_input)
    params = {}

    if intent == "play_song":
        # Try SpaCy first
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG"]:
                params["artist"] = ent.text
        # Fallback: regex for "by <artist>"
        match = re.search(r"by ([A-Za-z0-9\s]+)", user_input, re.IGNORECASE)
        if match and "artist" not in params:
            params["artist"] = match.group(1).strip()

    elif intent == "get_weather":
        for ent in doc.ents:
            if ent.label_ == "GPE":
                params["location"] = ent.text

    elif intent == "add_event":
        # Look for time/date + event name
        for ent in doc.ents:
            if ent.label_ in ["TIME", "DATE"]:
                params["datetime"] = ent.text
        # Grab event title (simplified: everything before/after datetime)
        if "datetime" in params:
            params["event"] = user_input.replace(params["datetime"], "").strip()

    elif intent == "create_todo":
        # Just take the task description after "add" or "put"
        match = re.search(r"(add|put|create|make)\s(.+)", user_input, re.IGNORECASE)
        if match:
            params["task"] = match.group(2).strip()
    elif intent == "calculate":
        # Extract math expression (numbers + operators)
        expr = re.findall(r"[0-9\+\-\*/\^\%\(\)\.\s]+", user_input)
        if expr:
            params["expression"] = "".join(expr).strip()

    return params