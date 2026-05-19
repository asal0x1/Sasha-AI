
import datetime
import random
import threading
import time
import webbrowser

import pyautogui
import speech_recognition as sr
import pyttsx3

WAKE_WORDS = ['hey sasha', 'sash', 'sasha']

history = []
scrolling = False
waiting_message_for = None

engine = pyttsx3.init()


def speek(text):
    print("Gono:", text)

    engine = pyttsx3.init('sapi5')
    engine.setProperty('volume', 1.0)
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def listen(timeout=5):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, phrase_time_limit=timeout)

        try:
            text = r.recognize_google(audio, language='en-US')
            print("You:", text)
            return text.lower()
        except:
            return ""


def scroll_worker(direction):
    global scrolling

    while scrolling:
        if direction == "down":
            pyautogui.scroll(-300)
        else:
            pyautogui.scroll(300)

        time.sleep(0.5)



def greet():
    return random.choice([
        "Hello, I'm listening.",
        "Hi, How can I help you?.",
        "Go ahead, I'm listening",
    ])


def get_time():
    now = datetime.datetime.now()
    return f"The time is {now.hour}: {now.minute}"


def detect_intent(text: str):
    if "hello" in text:
        return "greet"

    if "time" in text:
        return "time"

    if "youtube" in text:
        return "youtube"

    if "google" in text:
        return "google"

    if "scroll down" in text:
        return "scroll_down"

    if "scroll up" in text:
        return "scroll_up"

    if "stop" in text:
        return "scroll_stop"

    if "exit" in text:
        return "exit"

    return "unknown"


def handle_intent(intent):
    global scrolling

    if intent == "greet":
        return greet()

    if intent == "time":
        return get_time()

    if intent == "youtube":
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"

    if intent == "google":
        webbrowser.open("https://google.com")
        return "Opening Google"

    if intent == "scroll_down":
        scrolling = True
        threading.Thread(target=scroll_worker, args=("down",), daemon=True).start()
        return "Scrolling down"

    if intent == "scroll_up":
        scrolling = True
        threading.Thread(target=scroll_worker, args=("up",), daemon=True).start()
        return "Scrolling up"

    if intent == "scroll_stop":
        scrolling = False
        return "Stopped scrolling"

    return "I didn't understand"


def main():
    speek("Assistant started")

    active = False

    while True:
        msg = listen()

        if not msg:
            continue

        if not active:
            if any(w in msg for w in WAKE_WORDS):
                active = True
            continue

        intent = detect_intent(msg)

        if intent == "exit":
            speek("Goodbye!")
            active = False
            continue

        speek(handle_intent(intent))


if __name__ == "__main__":
    main()

