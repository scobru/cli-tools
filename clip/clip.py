#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pyperclip
import json
from pathlib import Path

# --- FIXED FILE PATH ---
HOME_DIR = Path.home()
HISTORY_FILE_PATH = HOME_DIR / "clipboard_history.json"


def read_history():
    """Reads the history list from the JSON file at its fixed location."""
    try:
        with open(HISTORY_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_history(history_list):
    """Writes the history list back to the JSON file at its fixed location."""
    with open(HISTORY_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(history_list, f, indent=2)

# --- MODIFIED FUNCTION ---
def save_content(content=None):
    """Saves a new item to the history.
    If content is provided, it saves that.
    Otherwise, it saves the content from the clipboard.
    """
    if content is None:
        content = pyperclip.paste() # Get from clipboard if no content is passed

    if not content.strip():
        print("📋 No content to save.")
        return

    history = read_history()
    history.append(content)
    write_history(history)
    print("✅ Content saved as a single item.")

def list_history():
    """Displays the saved clipboard history."""
    history = read_history()
    if not history:
        print("📖 History is empty.")
        return

    print("--- 📖 Clipboard History ---")
    for i, item in enumerate(history):
        first_line = item.strip().split('\n')[0]
        truncated_line = first_line[:70]
        print(f"{i + 1}: {truncated_line}...")

def get_item(item_number):
    """Copies a specific item from the history back to the clipboard."""
    history = read_history()
    try:
        index = int(item_number) - 1
        if 0 <= index < len(history):
            pyperclip.copy(history[index])
            print(f"✅ Item {index + 1} copied to clipboard.")
        else:
            print("❌ Invalid number.")
    except (ValueError, IndexError):
        print("❌ You must enter a valid number from the list.")

def delete_item(item_number):
    """Deletes a specific item from the history."""
    history = read_history()
    try:
        index = int(item_number) - 1
        if 0 <= index < len(history):
            history.pop(index)
            write_history(history)
            print(f"🗑️  Item {index + 1} deleted from history.")
        else:
            print("❌ Invalid number. Nothing to delete.")
    except (ValueError, IndexError):
        print("❌ You must enter a valid number from the list.")

def clear_history():
    """Clears the entire clipboard history."""
    write_history([])
    print("🗑️  Entire history cleared successfully.")

def show_help():
    """Prints the help message."""
    print("--- Clipboard Manager ---")
    print("Usage: clip [command]")
    print("\nAvailable commands:")
    print("  save           Saves the current clipboard content")
    print("  put <text>     Saves the provided text directly") # <-- NEW HELP TEXT
    print("  list           Shows the saved history")
    print("  get <n>        Copies item n from the history")
    print("  delete <n>     Deletes item n from the history")
    print("  clear          Deletes the entire history")

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        show_help()
    else:
        command = args[1]
        if command == "save":
            save_content() # Calls the function without arguments
        # --- NEW COMMAND ---
        elif command == "put":
            if len(args) > 2:
                # Join all arguments after 'put' into a single string
                text_to_save = " ".join(args[2:])
                save_content(content=text_to_save) # Calls with content
            else:
                print("❌ You must provide text to save. Ex: 'clip put my new item'.")
        elif command == "list":
            list_history()
        elif command == "get":
            if len(args) > 2:
                get_item(args[2])
            else:
                print("❌ Specify an item number.")
        elif command == "delete":
            if len(args) > 2:
                delete_item(args[2])
            else:
                print("❌ Specify an item number.")
        elif command == "clear":
            clear_history()
        else:
            show_help()
