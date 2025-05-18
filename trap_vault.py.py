import os
import time
import logging
import pyautogui
from tqdm import tqdm
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# --- CONFIG ---
TRAP_FOLDER = r"C:\HackerTrap\My Passwords"
TRAP_FILE = "Passwords.txt"
FULL_PATH = os.path.join(TRAP_FOLDER, TRAP_FILE)
LOG_FILE = r"C:\HackerTrap\access_log.txt"
SCREENSHOT_FOLDER = r"C:\HackerTrap\screenshots"

# --- SETUP ---
os.makedirs(TRAP_FOLDER, exist_ok=True)
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
if not os.path.exists(FULL_PATH):
    open(FULL_PATH, "w").close()

# --- LOGGER ---
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# --- TRIGGERED ACTION ---
def triggered_response():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"[{now}] File accessed: {FULL_PATH}")

    shot_path = os.path.join(SCREENSHOT_FOLDER, f"screenshot_{int(time.time())}.png")
    pyautogui.screenshot(shot_path)

    pyautogui.alert("You’ve been hacked! Your activity is being monitored.", "WARNING")

    for i in tqdm(range(100), desc="Encrypting files...", ncols=70):
        time.sleep(0.05)

    os.system("rundll32.exe user32.dll,LockWorkStation")

# --- WATCHER ---
class TrapHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == FULL_PATH:
            triggered_response()

# --- MAIN ---
def watch_trap():
    observer = Observer()
    observer.schedule(TrapHandler(), TRAP_FOLDER, recursive=False)
    observer.start()
    print(f"[*] Watching for access to: {FULL_PATH}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    watch_trap()
