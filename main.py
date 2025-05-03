import os
import eel
import webbrowser
import threading
import time
from enginee.featuers import *
from enginee.config import *
from enginee.command import *
from enginee.hotword import start_hotword_detection
from enginee.keyboard_trigger import start_keyboard_listener

eel.init("www")

# Start the eel app in non-blocking mode
eel.start('index.html', mode=None, host="localhost", port=8000, block=False)

@eel.expose
def play_sound():
    try:
        playAssistantSound()
        return {"status": "success"}
    except Exception as e:
        print(f"[ERROR] play_sound(): {e}")
        return {"status": "error", "message": str(e)}


# Open the Chrome App view
os.system('start msedge.exe --app="http://localhost:8000/index.html"')

# ✅ Start keyboard listener in a thread
threading.Thread(target=start_keyboard_listener, daemon=True).start()

# ✅ Start hotword detection after a short delay
def delayed_hotword_start():
    time.sleep(3)  # Wait 3 seconds for everything to load
    start_hotword_detection()

threading.Thread(target=delayed_hotword_start, daemon=True).start()

# Block main thread to keep the app running
eel.start('index.html', mode=None, host="localhost", block=True)
