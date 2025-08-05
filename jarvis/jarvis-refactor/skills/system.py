import os, subprocess, webbrowser, glob
from pathlib import Path

APP_MAP = {
    # Windows File Explorer
    "file explorer": {
        "paths": [r"explorer.exe"],
        "url": "https://support.microsoft.com/en-us/windows/file-explorer-in-windows-10-5e3d2f8b-1e4c-4e4e-8c1e-3b8b6b8a3c7e"
    },
    "explorer": {
        "paths": [r"explorer.exe"],
        "url": "https://support.microsoft.com/en-us/windows/file-explorer-in-windows-10-5e3d2f8b-1e4c-4e4e-8c1e-3b8b6b8a3c7e"
    },
    "windows explorer": {
        "paths": [r"explorer.exe"],
        "url": "https://support.microsoft.com/en-us/windows/file-explorer-in-windows-10-5e3d2f8b-1e4c-4e4e-8c1e-3b8b6b8a3c7e"
    },
    # Notepad
    "notepad": {
        "paths": [r"notepad.exe"],
        "url": "https://www.microsoft.com/en-us/p/windows-notepad/9msmlrh6lzf3"
    },
    # Calculator
    "calculator": {
        "paths": [r"calc.exe"],
        "url": "https://www.microsoft.com/en-us/p/windows-calculator/9wzdncrfhvn5"
    },
    # Paint
    "paint": {
        "paths": [r"mspaint.exe"],
        "url": "https://www.microsoft.com/en-us/p/paint/9pcfs5b6t72h"
    },
    # Command Prompt
    "command prompt": {
        "paths": [r"cmd.exe"],
        "url": "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd"
    },
    "cmd": {
        "paths": [r"cmd.exe"],
        "url": "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd"
    },
    # PowerShell
    "powershell": {
        "paths": [r"powershell.exe"],
        "url": "https://learn.microsoft.com/en-us/powershell/"
    },
    # WordPad
    "wordpad": {
        "paths": [r"write.exe"],
        "url": "https://support.microsoft.com/en-us/windows/wordpad-overview-0b7b6c4a-8b3e-4c2b-8e7b-2b8b6b8a3c7e"
    },
    # Task Manager
    "task manager": {
        "paths": [r"taskmgr.exe"],
        "url": "https://support.microsoft.com/en-us/windows/open-task-manager-in-windows-10-6b919b1a-2a5a-4c2b-8e7b-2b8b6b8a3c7e"
    },
    # Snipping Tool
    "snipping tool": {
        "paths": [r"SnippingTool.exe"],
        "url": "https://support.microsoft.com/en-us/windows/open-snipping-tool-and-take-a-screenshot-00246869-00e2-4e9a-bf5a-5b0b5b6b8a3c"
    },
    # Windows Media Player
    "windows media player": {
        "paths": [r"wmplayer.exe"],
        "url": "https://support.microsoft.com/en-us/windows/windows-media-player-12-3b8b6b8a3c7e"
    },
    # Control Panel
    "control panel": {
        "paths": [r"control.exe"],
        "url": "https://support.microsoft.com/en-us/windows/control-panel-in-windows-10-3b8b6b8a3c7e"
    },
    "youtube": {
        "paths": [
            r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Web Applications\_crx_*\\YouTube.exe",
            r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Web Applications\_crx_*\\YouTube.exe"
        ],
        "url": "https://youtube.com"
    },
    "spotify": {
        "paths": [r"C:\\Users\\%USERNAME%\\AppData\\Roaming\\Spotify\\Spotify.exe"],
        "url": "https://open.spotify.com"
    },
    "whatsapp": {
        "paths": [r"C:\\Users\\%USERNAME%\\AppData\\Local\\WhatsApp\\WhatsApp.exe"],
        "url": "https://web.whatsapp.com"
    },
    "vscode": {
        "paths": [
            r"C:\\Program Files\\Microsoft VS Code\\Code.exe",
            r"C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
            "code"
        ],
        "url": "https://vscode.dev"
    },
    "python idle": {
        "paths": [r"C:\\Python312\\Lib\\idlelib\\idle.bat"],
        "url": "https://python.org"
    },
}

def _expand(p):
    p = os.path.expandvars(p)
    return glob.glob(p) if any(ch in p for ch in "*?") else [p]

def _launch(exe_or_cmd):
    try:
        if Path(exe_or_cmd).is_file():
            subprocess.Popen([exe_or_cmd])
        else:
            subprocess.Popen(exe_or_cmd, shell=True)
        return True
    except Exception:
        return False

def open_any(target: str):
    orig_target = target.strip()
    target_key = orig_target.lower().replace(".com", "").replace(".exe", "").strip()
    print(f"[DEBUG] Requested to open: '{orig_target}', target_key: '{target_key}'")
    app_info = APP_MAP.get(target_key)
    if not app_info and target_key.startswith("the "):
        app_info = APP_MAP.get(target_key[4:])
    tried_paths = []
    if app_info:
        print(f"[DEBUG] Found app_info for '{target_key}': {app_info}")
        for raw in app_info.get("paths", []):
            for p in _expand(raw):
                tried_paths.append(p)
                print(f"[DEBUG] Trying to launch: {p}")
                if _launch(p):
                    print(f"[DEBUG] Successfully launched: {p}")
                    return f"Opened {orig_target} via {p}"
        fallback_url = app_info.get("url")
        print(f"[DEBUG] No executable found, will try URL: {fallback_url}")
    else:
        fallback_url = f"https://{target_key.replace(' ', '')}.com"
        print(f"[DEBUG] No app_info for '{target_key}', fallback_url: {fallback_url}")
    opened = webbrowser.open_new_tab(fallback_url)
    if not opened:
        opened = webbrowser.open(fallback_url)
    if tried_paths:
        msg = f"App not found for '{orig_target}' (tried: {tried_paths}). Tried to open {fallback_url} in your browser."
        print(f"[DEBUG] {msg}")
        return f"🌐 {msg}"
    else:
        msg = f"No app rule for '{orig_target}'. Tried to open {fallback_url} in your browser."
        print(f"[DEBUG] {msg}")
        return f"🌐 {msg}"

def perform_computer_task(command):
    import difflib
    from fuzzywuzzy import fuzz
    command = command.lower().strip()
    # Define possible intents and their keywords
    intents = {
        'open': ['open', 'launch', 'start'],
        'list_files': ['list files in', 'show files in', 'what files are in'],
        'move_mouse': ['move mouse to', 'move cursor to'],
        'click_mouse': ['click mouse', 'mouse click', 'press mouse'],
        'type': ['type', 'write', 'input'],
    }
    # Fuzzy intent detection
    def match_intent(cmd):
        for intent, phrases in intents.items():
            for phrase in phrases:
                if fuzz.partial_ratio(cmd, phrase) > 85 or cmd.startswith(phrase):
                    return intent, phrase
        return None, None
    intent, phrase = match_intent(command)
    try:
        if intent == 'open':
            app = command[len(phrase):].strip()
            return open_any(app)
        elif intent == 'list_files':
            folder = command[len(phrase):].strip()
            files = os.listdir(folder)
            return f"Files in {folder}:\n" + "\n".join(files)
        elif intent == 'move_mouse':
            parts = command[len(phrase):].split(",")
            x, y = int(parts[0].strip()), int(parts[1].strip())
            import pyautogui
            pyautogui.moveTo(x, y)
            return f"Moved mouse to ({x}, {y})."
        elif intent == 'click_mouse':
            import pyautogui
            pyautogui.click()
            return "Mouse clicked."
        elif intent == 'type':
            import pyautogui
            text = command[len(phrase):].strip()
            pyautogui.write(text)
            return f"Typed: {text}"
        else:
            # Try to match to an app name for open
            for app in APP_MAP.keys():
                if fuzz.partial_ratio(command, app) > 85:
                    return open_any(app)
            return "Sorry, I didn't understand the command."
    except Exception as e:
        return f"❌ Error: {e}"
