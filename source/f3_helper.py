import time
import threading
from pynput import keyboard
import tkinter as tk
from tkinter import ttk
import sys
import os
import psutil

KEY_PRESS_DELAY = 0.05
TRIGGER_KEY = 'o'
INITIAL_DELAY_SECONDS = 0.1
DEFAULT_FIXED_SECOND_KEY = 'g'
KEY_MAP = {
    'escape': keyboard.Key.esc,
    # 'f4' : keyboard.Key.f4,
}

def is_minecraft_running():
    minecraft_process_names = [
        "javaw.exe",  # Common for Minecraft Java Edition
        "minecraft.windows.exe", # For Minecraft Bedrock Edition (Windows 10/11)
        
        # Can include any other Launchers
    ]
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() in minecraft_process_names:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False

def press_f3_and_key(second_key_input):
    display_key = second_key_input.upper() if isinstance(second_key_input, str) else str(second_key_input).replace('Key.', '').upper()
    status_label.config(text=f"Attempting to simulate F3 + {display_key}...")
    root.update_idletasks()
    print(f"\nAttempting to simulate F3 + {display_key}...")

    try:
        controller = keyboard.Controller()
        controller.press(keyboard.Key.f3)
        time.sleep(KEY_PRESS_DELAY)
        controller.press(second_key_input)
        time.sleep(KEY_PRESS_DELAY)
        controller.release(second_key_input)
        time.sleep(KEY_PRESS_DELAY)

        controller.release(keyboard.Key.f3)
        status_label.config(text=f"Successfully simulated F3 + {display_key}.")
        root.update_idletasks()
        print(f"Successfully simulated F3 + {display_key}.")

    except Exception as e:
        error_msg = f"An error occurred during key simulation: {e}"
        status_label.config(text=error_msg)
        root.update_idletasks()
        print(error_msg)
        controller.release(keyboard.Key.f3)

def simulate_shortcut_after_delay():
    selected_key_str = selected_key_var.get().lower()
    key_to_press = KEY_MAP.get(selected_key_str, selected_key_str)

    press_f3_and_key(key_to_press)

    status_label.config(text=f"Press '{TRIGGER_KEY.upper()}' to toggle F3 + selected key.")
    root.update_idletasks()

def on_press(key):
    try:
        if isinstance(TRIGGER_KEY, str) and hasattr(key, 'char') and key.char and key.char.lower() == TRIGGER_KEY.lower():
            status_label.config(text=f"'{TRIGGER_KEY.upper()}' pressed. Delaying {INITIAL_DELAY_SECONDS}s...")
            root.update_idletasks()
            root.after(int(INITIAL_DELAY_SECONDS * 1000), simulate_shortcut_after_delay)

        elif isinstance(TRIGGER_KEY, keyboard.Key) and key == TRIGGER_KEY:
            trigger_display = str(TRIGGER_KEY).replace('Key.', '').replace('_gr', ' Alt')
            status_label.config(text=f"{trigger_display} pressed. Delaying {INITIAL_DELAY_SECONDS}s...")
            root.update_idletasks()
            root.after(int(INITIAL_DELAY_SECONDS * 1000), simulate_shortcut_after_delay)

    except Exception as e:
        print(f"Error in on_press: {e}")
        status_label.config(text=f"Error: {e}")
        root.update_idletasks()

def on_release(key):
    pass

if __name__ == "__main__":
    if not is_minecraft_running():
        error_root = tk.Tk()
        error_root.title("Error")
        error_root.geometry("300x100")
        error_root.resizable(False, False)
        error_root.grid_rowconfigure(0, weight=1)
        error_root.grid_columnconfigure(0, weight=1)

        error_label = ttk.Label(error_root, text="Minecraft is not running.\nPlease open Minecraft first.", justify=tk.CENTER)
        error_label.grid(row=0, column=0, padx=10, pady=10)

        print("Error: Minecraft is not running. Please open Minecraft first.")
        error_root.mainloop()
        sys.exit(1)

    root = tk.Tk()
    root.title("Minecraft F3 Shortcut Helper")

    root.geometry("350x180")
    root.resizable(False, False)

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_columnconfigure(0, weight=1)

    f3_keys = ['A', 'B', 'C', 'D', 'G', 'H', 'Q', 'I', 'N', 'P', 'T', 'Escape'] # '1', '2', '3', '4', '5', '6', '7', '8', '9', 
    selected_key_var = tk.StringVar(root)

    key_label = ttk.Label(root, text="Select F3 Combination Key:")
    key_label.grid(row=0, column=0, pady=(10, 0))
    key_dropdown = ttk.Combobox(root, textvariable=selected_key_var, values=f3_keys, state="readonly", width=15)
    key_dropdown.grid(row=1, column=0, pady=(0, 10))

    if DEFAULT_FIXED_SECOND_KEY.upper() in f3_keys:
        key_dropdown.set(DEFAULT_FIXED_SECOND_KEY.upper())
    else:
        key_dropdown.set(f3_keys[0])

    info_label = ttk.Label(root, text=f"Press the '{TRIGGER_KEY.upper()}' key in Minecraft\nto activate the F3 + selected key shortcut.", justify=tk.CENTER)
    info_label.grid(row=2, column=0, pady=(5, 5))
    status_label = ttk.Label(root, text=f"Ready. Select a key above.")
    status_label.grid(row=3, column=0, pady=(0, 10))

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    root.mainloop()
    if listener.running:
        listener.stop()
    print("Script finished.")
