import asyncio
from actions import plan_actions, execute_actions
import sounddevice as sd
import numpy as np
import speech_recognition as sr

# Map simple voice commands to intents
VOICE_INTENT_MAP = {
    "search product": "search_product",
    "google search": "search_google",
    "youtube search": "search_youtube",
    "play spotify": "play_spotify",
    "take screenshot": "take_screenshot",
    "speak": "speak_text",
    "fun mode": "fun_mode",
    "exit": "exit",
    "stop": "exit"
}

def get_voice_input(duration=5):
    """Record audio using sounddevice and recognize speech using Google."""
    recognizer = sr.Recognizer()
    fs = 44100  # Sample rate
    print("Listening... Speak your command:")
    
    # Record audio
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    
    # Convert to AudioData for speech_recognition
    audio_data = sr.AudioData(recording.tobytes(), fs, 2)
    
    try:
        command = recognizer.recognize_google(audio_data)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
    return None

def map_command_to_intent(command):
    for key_phrase, intent in VOICE_INTENT_MAP.items():
        if key_phrase in command:
            return intent
    return "unknown"

async def main():
    print("Jarvis Voice Agent activated. Listening for commands...")
    while True:
        command = get_voice_input()
        if not command:
            continue

        intent = map_command_to_intent(command)
        entities = {}

        # Extract entities from command
        if intent in ["search_product", "search_google", "search_youtube", "play_spotify"]:
            if intent == "search_product":
                entities["product"] = command.replace("search product", "").strip()
            elif intent == "search_google":
                entities["query"] = command.replace("google search", "").strip()
            elif intent == "search_youtube":
                entities["query"] = command.replace("youtube search", "").strip()
            elif intent == "play_spotify":
                entities["song"] = command.replace("play spotify", "").strip()
        elif intent == "speak_text":
            entities["text"] = command.replace("speak", "").strip()
        elif intent == "take_screenshot":
            entities["filename"] = "screenshot.png"

        intent_data = {"intent": intent, "entities": entities}

        print(f"Executing Intent: {intent_data['intent']}")
        print(f"Entities: {intent_data['entities']}")

        # Plan and execute actions asynchronously
        actions = plan_actions(intent_data)
        await asyncio.to_thread(execute_actions, actions)

        # Stop if user says exit/stop
        if intent == "exit":
            print("Exiting Jarvis Voice Agent...")
            break

if __name__ == "__main__":
    asyncio.run(main())

