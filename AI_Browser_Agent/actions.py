from playwright.async_api import async_playwright
from gtts import gTTS
import os
import asyncio
import webbrowser
import pywhatkit  # For playing first YouTube video

# ---------------- TTS ----------------
def speak(text):
    """Convert text to speech using gTTS and play it on macOS."""
    if not text:
        return
    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")
    os.system("afplay temp.mp3")  # macOS playback

# ---------------- Action Planning ----------------
def plan_actions(intent_data):
    """
    Return a list of actions to execute based on intent_data.
    intent_data = {"intent": str, "entities": dict}
    """
    intent = intent_data.get("intent")
    entities = intent_data.get("entities", {})

    actions = []

    if intent == "search_product":
        actions.append(("search_product", entities))
    elif intent == "search_google":
        actions.append(("search_google", entities))
    elif intent == "search_youtube":
        actions.append(("search_youtube", entities))
    elif intent == "play_spotify":
        actions.append(("play_spotify", entities))
    elif intent == "speak_text":
        actions.append(("speak_text", entities))
    elif intent == "take_screenshot":
        actions.append(("take_screenshot", entities))
    elif intent == "fun_mode":
        actions.append(("fun_mode", entities))
    elif intent == "exit":
        actions.append(("exit", entities))
    else:
        actions.append(("unknown", entities))

    return actions

# ---------------- Action Execution ----------------
def execute_actions(actions):
    """Execute the planned actions."""
    for action, data in actions:
        if action == "search_product":
            product = data.get("product", "")
            if product:
                url = f"https://www.amazon.com/s?k={product.replace(' ', '+')}"
                print(f"Opening Amazon search for '{product}'...")
                webbrowser.open(url)
                speak(f"Searching for {product} on Amazon")
            else:
                print("No product specified.")

        elif action == "search_google":
            query = data.get("query", "")
            if query:
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                print(f"Opening Google search for '{query}'...")
                webbrowser.open(url)
                speak(f"Searching Google for {query}")
            else:
                print("No query specified.")

        elif action == "search_youtube":
            query = data.get("query", "")
            if query:
                print(f"Playing first YouTube video for '{query}'...")
                speak(f"Playing {query} on YouTube")
                pywhatkit.playonyt(query)  # Opens the first video automatically
            else:
                print("No query specified.")

        elif action == "play_spotify":
            song = data.get("song", "")
            if song:
                print(f"Playing '{song}' on Spotify...")
                speak(f"Playing {song} on Spotify")
                asyncio.run(play_spotify_song(song))
            else:
                print("No song specified.")

        elif action == "speak_text":
            text = data.get("text", "")
            if text:
                speak(text)
            else:
                print("No text provided.")

        elif action == "take_screenshot":
            filename = data.get("filename", "screenshot.png")
            # macOS screenshot via os command
            os.system(f"screencapture {filename}")
            speak(f"Screenshot saved as {filename}")
            print(f"Screenshot saved as {filename}")

        elif action == "fun_mode":
            print("Activating fun mode...")
            speak("Let's have some fun!")
            # Add fun interactions here

        elif action == "exit":
            speak("Exiting Jarvis Voice Agent.")

        elif action == "unknown":
            print("Unknown command received.")
            speak("Sorry, I did not understand that command.")

async def play_spotify_song(song_name):
    """Play the first Spotify song result (with persistent login)."""
    if not song_name:
        print("No song specified.")
        return

    print(f"🎵 Searching for '{song_name}' on Spotify...")

    try:
        user_data_dir = os.path.join(os.getcwd(), "spotify_profile")

        async with async_playwright() as p:
            #  Launch persistent context (saves login session)
            browser = await p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=False,
                args=["--autoplay-policy=no-user-gesture-required"]
            )
            page = await browser.new_page()

            # Go to Spotify search page
            await page.goto("https://open.spotify.com/search", timeout=60000)

            # Detect if user not logged in
            if "login" in page.url.lower():
                print(" Please log in to Spotify (only first time).")
                await page.wait_for_timeout(15000)  # 15 sec to log in manually
                print(" Login session will be saved for next time.")

            #  Wait for search input
            await page.wait_for_selector("input[data-testid='search-input']", timeout=30000)
            await page.fill("input[data-testid='search-input']", song_name)
            await asyncio.sleep(1)
            await page.keyboard.press("Enter")
            await asyncio.sleep(3)

            # Click the first play button in "Songs" section
            try:
                await page.wait_for_selector("div[data-testid='tracklist-row'] button", timeout=10000)
                buttons = await page.query_selector_all("div[data-testid='tracklist-row'] button")
                if buttons:
                    await buttons[0].click()
                    print(f" Now playing: {song_name}")
                else:
                    print("⚠️ Could not find song play button.")
            except Exception as e:
                print(" Could not find song result:", e)

            await asyncio.sleep(60)  # let the song play for a minute
            await browser.close()

    except Exception as e:
        print(f"⚠️ Error in Spotify playback: {e}")
