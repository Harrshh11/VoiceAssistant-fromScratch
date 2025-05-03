import speech_recognition as sr
import eel
import time
import re
import os
from difflib import get_close_matches

from enginee.speech_utils import speak
from enginee.featuers import (
    openCommand, PlayYoutube, send_whatsapp_message,
    make_whatsapp_call, get_all_contact_names
)

# Global flag to control loop termination
stop_listening = False

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            print("Timeout, no speech detected.")
            return ""
    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        time.sleep(1)
        return query.lower()
    except Exception:
        print("Recognition failed.")
        eel.DisplayMessage("Didn't catch that! Try again.")
        return ""

def fuzzy_match_name(name):
    contacts = get_all_contact_names()
    matches = get_close_matches(name, contacts, n=1, cutoff=0.6)
    return matches[0] if matches else None

@eel.expose
def go_back_triggered():
    global stop_listening
    stop_listening = True
    print("🔙 Going back to main page. Stopping assistant...")

@eel.expose
def allCommands(query=None):
    global stop_listening
    stop_listening = False

    while not stop_listening:
        if query is None:
            query = take_command()
        if not query:
            speak("I didn't catch that. Please say again.")
            eel.Showhood()
            break

        print(f"Processing query: {query}")
        
        if "siri keep quiet" in query or "stop listening" in query:
            speak("Okay, I will remain silent.")
            stop_listening = True
            eel.Showhood()
            break

        msg_match = re.search(r"(?:send message to|message|text) (.*?) (?:saying|says|that)? (.+)", query)
        if msg_match:
            contact_name = msg_match.group(1).strip()
            message = msg_match.group(2).strip()
            matched = fuzzy_match_name(contact_name)
            if matched:
                send_whatsapp_message(matched, message)
            else:
                speak("I couldn't find that contact in your database.")
            eel.Showhood()
            query = None
            continue

        if "call" in query and "whatsapp" in query:
            call_match = re.search(r"call (.*?) on whatsapp", query)
            if call_match:
                contact_name = call_match.group(1).strip()
                matched = fuzzy_match_name(contact_name)
                if matched:
                    make_whatsapp_call(matched)
                else:
                    speak("I couldn't find that contact in your database.")
            eel.Showhood()
            query = None
            continue

        if "go back" in query or "previous page" in query or "move to main page" in query:
            speak("Taking you back to the main screen.")
            eel.go_back()
            stop_listening = True
            break

        if "close" in query:
            app_match = re.search(r"close (.+)", query)
            if app_match:
                app_name = app_match.group(1).strip().lower()

                app_processes = {
                    "youtube": "chrome.exe",
                    "browser": "chrome.exe",
                    "notepad": "notepad.exe",
                    "spotify": "spotify.exe",
                    "whatsapp": "whatsapp.exe"
                }

                process_to_kill = app_processes.get(app_name)
                if process_to_kill:
                    os.system(f"taskkill /f /im {process_to_kill}")
                    speak(f"Closing {app_name}")
                else:
                    speak(f"I don't know how to close {app_name}")
            else:
                speak("Please specify what to close.")
            eel.Showhood()
            query = None
            continue

        if "open" in query:
            openCommand(query)
        elif "on youtube" in query:
            PlayYoutube(query)
        else:
            speak("I didn't catch that. Please say again.")

        eel.Showhood()
        query = None
