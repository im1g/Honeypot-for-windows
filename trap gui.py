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
TRAP_FILE_1 = "All passwords saved.txt"
TRAP_FILE_2 = "all passwords saved updated.txt"
TRAP_PATH_1 = os.path.join(TRAP_FOLDER, TRAP_FILE_1)
TRAP_PATH_2 = os.path.join(TRAP_FOLDER, TRAP_FILE_2)
LOG_FILE = r"C:\HackerTrap\access_log.txt"
SCREENSHOT_FOLDER = r"C:\HackerTrap\screenshots"

# --- SETUP ---
os.makedirs(TRAP_FOLDER, exist_ok=True)
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

for path in [TRAP_PATH_1, TRAP_PATH_2]:
    if not os.path.exists(path):
        open(path, "w").close()

logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# --- TRIGGERED ACTION ---
def triggered_response(triggered_file):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"[{now}] File accessed: {triggered_file}")

    screenshot_path = os.path.join(SCREENSHOT_FOLDER, f"screenshot_{int(time.time())}.png")
    pyautogui.screenshot(screenshot_path)

    pyautogui.alert("You’ve been hacked! Your activity is being monitored.", "WARNING")

    for _ in tqdm(range(100), desc="Encrypting files...", ncols=70):
        time.sleep(0.05)

    os.system("rundll32.exe user32.dll,LockWorkStation")

# --- WATCHER ---
class TrapHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.lower() in [TRAP_PATH_1.lower(), TRAP_PATH_2.lower()]:
            triggered_response(event.src_path)

# --- MAIN ---
def watch_trap():
    observer = Observer()
    observer.schedule(TrapHandler(), TRAP_FOLDER, recursive=False)
    observer.start()
    print(f"[*] Watching for access to:\n  - {TRAP_PATH_1}\n  - {TRAP_PATH_2}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    watch_trap()
