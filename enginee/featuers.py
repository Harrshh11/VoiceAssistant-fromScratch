import eel
import re
import pywhatkit as kit
import pygame
import os
import webbrowser
import sqlite3
import pyautogui
import time
from playsound import playsound
from enginee.speech_utils import speak
from enginee.config import ASSISTANT_NAME

# Connect to the SQLite database
def get_db_connection():
    return sqlite3.connect("Sara.db")

def playAssistantSound():
    music_dir = r"C:\Users\HP-YC\Desktop\Sara\www\assests\ttsMP3.com_VoiceText_2025-4-27_13-59-16.mp3"
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(music_dir)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing sound: {e}")

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.strip().lower()

    if not query:
        speak("Command not understood.")
        return

    speak("Opening " + query)

    # Check in sys_command table
    with get_db_connection() as con:
        cursor = con.cursor()
        cursor.execute("SELECT path FROM sys_command WHERE name = ?", (query,))
        sys_result = cursor.fetchone()

        if sys_result:
            os.system("start " + sys_result[0])
            return

        # Check in web_command table
        cursor.execute("SELECT url FROM web_command WHERE name = ?", (query,))
        web_result = cursor.fetchone()

        if web_result:
            webbrowser.open(web_result[0])
            return

    # Special case for WhatsApp (Microsoft Store version)
    if "whatsapp" in query:
        try:
            os.system("start shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App")
            return
        except Exception as e:
            speak("WhatsApp is not found in the default path.")
            print("Error:", e)
            return

    # Special case for Spotify (Chrome-installed PWA)
    if "spotify" in query:
        try:
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            app_url = "https://open.spotify.com/"
            os.system(f'"{chrome_path}" --app={app_url}')
            return
        except Exception as e:
            speak("Spotify is not found or Chrome is missing.")
            print("Error:", e)
            return

    # If not found in DB or special case, try default open
    os.system('start ' + query)

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if search_term:
        speak("Playing " + search_term + " on YouTube")
        try:
            kit.playonyt(search_term)
        except Exception as e:
            speak("Failed to open YouTube")
            print("Error:", e)
    else:
        speak("Sorry, I couldn't understand the YouTube search command.")

def extract_yt_term(command):
    pattern = r"(?:play|search)\s+(.*?)\s+(?:on\s+youtube|on\s+YouTube|from\s+YouTube)"
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None

def send_whatsapp_message(contact_name, message):
    contact_name = contact_name.lower().strip()  # Normalize

    with get_db_connection() as con:
        cursor = con.cursor()
        cursor.execute("SELECT phone_number FROM contacts WHERE LOWER(name) = ?", (contact_name,))
        result = cursor.fetchone()

    if result:
        phone_number = result[0]
        speak(f"Sending message to {contact_name}")
        try:
            kit.sendwhatmsg_instantly(f"+91{phone_number}", message, wait_time=10, tab_close=True)
        except Exception as e:
            speak("Failed to send message on WhatsApp.")
            print("Error:", e)
    else:
        speak(f"I couldn't find {contact_name} in your contacts.")


def make_whatsapp_call(name):
    name = name.strip().lower()
    with get_db_connection() as con:
        cursor = con.cursor()
        cursor.execute("SELECT phone_number FROM contacts WHERE LOWER(name) LIKE ?", (f"%{name}%",))
        result = cursor.fetchone()

    if result:
        phone = result[0]
        speak(f"Opening WhatsApp chat with {name}. You can press the call button.")
        try:
            # Use WhatsApp Desktop URI scheme to open chat
            os.system(f'start whatsapp://send?phone=+91{phone}')
        except Exception as e:
            speak("Failed to open WhatsApp Desktop.")
            print("Error:", e)
    else:
        speak("Contact not found in the database.")

def get_all_contact_names():
    conn = sqlite3.connect("Sara.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM contacts")
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

def go_back_to_main_page():
    eel.go_back() 
    
    