import keyboard
from enginee.command import allCommands  # ✅ Import here

def start_keyboard_listener():
    print("Press Ctrl+Shift+S to activate Sara")
    keyboard.wait('ctrl+shift+s')
    print("Key detected!")
    allCommands()  # ✅ Direct call
