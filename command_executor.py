import subprocess
import pyautogui
import os
import re
import time
import json
import random
from llm_chat import query_llm
# Track last action to enable command chaining
last_action = ""

def get_founder_name():
    try:
        with open("friday_config.json", "r") as f:
            config = json.load(f)
        return config.get("founder_name", "Unknown")
    except Exception:
        return "Unknown"

def friendly_reply():
    responses = [
        "I'm doing great, Chinmay! Always ready to assist you with brilliance and speed.",
        "Feeling fantastic! Thanks for asking. What are we building today?",
        "All systems go. Just waiting for your next command, boss.",
        "Couldn't be better—especially when you're around!"
    ]
    return random.choice(responses)



def execute_command(command):
    global last_action
    command = command.lower()

    # Fixed paths for known apps
    app_paths = {
        "notepad": "C:\\Windows\\System32\\notepad.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "calculator": "C:\\Windows\\System32\\calc.exe",
        "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
        "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "paint": "C:\\Windows\\System32\\mspaint.exe",
        "command prompt": "C:\\Windows\\System32\\cmd.exe",
        "task manager": "C:\\Windows\\System32\\Taskmgr.exe",
        "file explorer": "C:\\Windows\\explorer.exe",
        "control panel": "C:\\Windows\\System32\\control.exe",
        "snipping tool": "C:\\Windows\\System32\\SnippingTool.exe",
        "windows media player": "C:\\Program Files\\Windows Media Player\\wmplayer.exe",
        "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        "vs code": "C:\\Users\\Chinmay\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
    }

    # Open known apps
    for app in app_paths:
        if f"open {app}" in command:
            try:
                subprocess.Popen(app_paths[app])
                last_action = f"{app}_opened"
                return f"Opening {app}."
            except Exception as e:
                return f"Failed to open {app}: {e}"

    # Open Recycle Bin
    if "open recycle bin" in command:
        try:
            subprocess.Popen(["explorer.exe", "shell:RecycleBinFolder"])
            last_action = "recycle_bin_opened"
            return "Opening Recycle Bin."
        except Exception as e:
            return f"Failed to open Recycle Bin: {e}"

    # Select all files (only if Recycle Bin was opened)
    if "select all" in command and last_action == "recycle_bin_opened":
        time.sleep(2)  # Allow window to focus
        pyautogui.hotkey('ctrl', 'a')
        last_action = "files_selected"
        return "Selected all files in Recycle Bin."

    # Delete selected files (only if files were selected)
    if "delete them all" in command and last_action == "files_selected":
        pyautogui.hotkey('shift', 'delete')
        time.sleep(1)
        pyautogui.press('enter')  # Confirm permanent deletion
        last_action = ""
        return "Deleted all selected files from Recycle Bin."

    # Delete file by full path
    if "delete" in command:
        match = re.search(r"delete (.+)", command)
        if match:
            filepath = match.group(1).strip().strip('"')
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                    return f"Deleted {filepath}."
                except Exception as e:
                    return f"Failed to delete {filepath}: {e}"
            else:
                return f"File not found: {filepath}"
        return "Please specify a valid file path to delete."

    # Respond to founder identity queries
    if "who is your founder" in command or "who created you" in command:
        return f"My founder is {get_founder_name()}. I'm proud to be built by him!"
    
    if "how are you" in command:
        return friendly_reply()
    
        # If no known command matched, use LLM
    return query_llm(command)

    return "Command not recognized. I can open apps, select files, and delete them when instructed."