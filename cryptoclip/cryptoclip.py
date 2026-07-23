#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import argparse
import threading
import signal

# Force stdout/stderr to use UTF-8 to prevent encoding crashes on Windows console when printing emojis
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# --- CRYPTOGRAPHY AND CLIPBOARD ---
from cryptography.fernet import Fernet
import pyperclip

# --- KEYBOARD LISTENER (DEFENSIVE) ---
try:
    from pynput import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False

# --- SYSTEM TRAY (DEFENSIVE) ---
try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False

# --- CONFIGURATION & KEY PRECEDENCE ---
DEFAULT_KEY = "cw_0Z65YWg6Wv0Cd-ahB6vWpgWMAuAhs58EvNMz0niM="
ACTIVE_KEY = DEFAULT_KEY
key_lock = threading.Lock()

def get_active_key():
    """Returns the current active Fernet key in a thread-safe manner."""
    with key_lock:
        return ACTIVE_KEY

def set_active_key(new_key):
    """Validates and sets the active Fernet key. Returns True if valid, False otherwise."""
    global ACTIVE_KEY
    trimmed = new_key.strip()
    try:
        # Validate key correctness by initializing Fernet
        Fernet(trimmed.encode('utf-8'))
        with key_lock:
            ACTIVE_KEY = trimmed
        return True
    except Exception:
        return False

def get_fernet():
    """Instantiates a Fernet object using the active key."""
    key = get_active_key()
    try:
        return Fernet(key.encode('utf-8'))
    except Exception:
        return None

# --- ACTIONS ---

def encrypt_text():
    """Encrypts the plain text currently in the clipboard using the active key."""
    try:
        plain_text = pyperclip.paste()
        if not plain_text:
            return
        
        # Avoid double encrypting already encrypted content using the same key
        fernet = get_fernet()
        if not fernet:
            print("⚠️ Error: Invalid Fernet key.")
            return

        try:
            # Check if it is already encrypted with our key
            fernet.decrypt(plain_text.strip().encode('utf-8'))
            print("💡 Clipboard already contains valid encrypted text using this key. Skipping.")
            return
        except Exception:
            pass

        encrypted_bytes = fernet.encrypt(plain_text.encode('utf-8'))
        encrypted_text = encrypted_bytes.decode('utf-8')
        pyperclip.copy(encrypted_text)
        print("\n🔐 Text encrypted and copied to clipboard!")
        print(f"   ► Original : {plain_text}")
        print(f"   ► Encrypted: {encrypted_text}")
        print("-" * 50)
    except Exception as e:
        print(f"⚠️ Error encrypting: {e}")

def decrypt_text():
    """Decrypts the cipher text currently in the clipboard using the active key."""
    try:
        encrypted_text = pyperclip.paste()
        if not encrypted_text:
            return
        
        fernet = get_fernet()
        if not fernet:
            print("⚠️ Error: Invalid Fernet key.")
            return

        try:
            decrypted_bytes = fernet.decrypt(encrypted_text.strip().encode('utf-8'))
            plain_text = decrypted_bytes.decode('utf-8')
            pyperclip.copy(plain_text)
            print("\n🔓 Text decrypted and copied to clipboard!")
            print(f"   ► Decrypted: {plain_text}")
            print("-" * 50)
        except Exception:
            print("⚠️ Unable to decrypt: text is not a valid Fernet token or key is invalid.")
    except Exception as e:
        print(f"⚠️ Error decrypting: {e}")

def generate_new_key():
    """Generates a new Fernet key, prints it, and copies it to clipboard."""
    try:
        new_key = Fernet.generate_key().decode('utf-8')
        print("\n🔑 New Fernet key generated:")
        print(f"   ► {new_key}")
        pyperclip.copy(new_key)
        print("📋 The new key has been copied to your clipboard!")
        print(f"💡 Set environment variable CRYPTO_CLIPBOARD_KEY=\"{new_key}\" to use it permanently.")
        print("-" * 50)
        return new_key
    except Exception as e:
        print(f"⚠️ Error generating key: {e}")
        return None

def load_key_from_clipboard():
    """Attempts to load a new active key from the text in the clipboard."""
    try:
        candidate = pyperclip.paste().strip()
        if set_active_key(candidate):
            print("\n🔑 Active key successfully updated from clipboard!")
            print(f"   ► Active Key: {candidate[:8]}...")
            print("-" * 50)
        else:
            print("\n⚠️ Invalid Fernet key in clipboard. Please copy a valid 32-byte Base64 key first.")
    except Exception as e:
        print(f"⚠️ Error loading key from clipboard: {e}")

# --- BACKGROUND MONITOR ---

def start_clipboard_monitor():
    """Launches the background thread monitoring clipboard for auto-decryption."""
    def monitor_loop():
        last_text = ""
        while True:
            try:
                time.sleep(0.5)
                current_text = pyperclip.paste()
                if current_text:
                    trimmed = current_text.strip()
                    if trimmed and trimmed != last_text:
                        last_text = trimmed
                        fernet = get_fernet()
                        if fernet:
                            try:
                                decrypted_bytes = fernet.decrypt(trimmed.encode('utf-8'))
                                plain_text = decrypted_bytes.decode('utf-8')
                                print("\n✨ [Clipboard Monitor] Encrypted text detected in clipboard!")
                                print(f"🔓 Decrypted (Console): {plain_text}")
                                print("💡 Press Ctrl + Shift + D to replace clipboard with decrypted text.")
                                print("-" * 50)
                            except Exception:
                                pass
            except Exception:
                pass

    monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    monitor_thread.start()

# --- SYSTEM TRAY ---

def create_tray_image():
    """Generates a simple 64x64 lock icon on the fly using PIL."""
    image = Image.new('RGB', (64, 64), color=(63, 81, 181)) # Indigo background
    draw = ImageDraw.Draw(image)
    # Draw lock body (white rectangle)
    draw.rectangle([(20, 28), (44, 52)], fill=(255, 255, 255))
    # Draw lock shackle (white arc)
    draw.arc([(24, 16), (40, 32)], 180, 360, fill=(255, 255, 255), width=4)
    return image

def exit_action(icon, item):
    """Action callback to stop tray icon and exit program."""
    print("Exiting CryptoClipboard...")
    icon.stop()
    os._exit(0)

def run_tray():
    """Starts the system tray icon loop. Blocks the current thread."""
    if not TRAY_AVAILABLE:
        print("⚠️ System tray GUI libraries (pystray / PIL) not available. Running in console-only mode.")
        while True:
            time.sleep(1)
        return

    try:
        image = create_tray_image()
        menu = pystray.Menu(
            pystray.MenuItem("🔐 Encrypt Clipboard (Ctrl+Shift+E)", lambda: encrypt_text()),
            pystray.MenuItem("🔓 Decrypt Clipboard (Ctrl+Shift+D)", lambda: decrypt_text()),
            pystray.MenuItem("🔑 Generate New Key (Ctrl+Shift+K)", lambda: generate_new_key()),
            pystray.MenuItem("📋 Load Key from Clipboard (Ctrl+Shift+I)", lambda: load_key_from_clipboard()),
            pystray.MenuItem("❌ Exit", exit_action)
        )
        icon = pystray.Icon("CryptoClipboard", image, "CryptoClipboard", menu)
        print("📌 System Tray Icon enabled.")
        icon.run()
    except Exception as e:
        print(f"⚠️ Could not create system tray icon: {e}")
        print("💡 Running in console-only mode.")
        while True:
            time.sleep(1)

# --- CLEAN EXIT SIGNAL HANDLERS ---

def signal_handler(sig, frame):
    """Graceful shutdown handler for terminal interrupts."""
    print("\nExiting CryptoClipboard...")
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# --- MAIN ENTRYPOINT ---

def main():
    # Support positional "genkey" subcommand to match original Rust behavior
    if len(sys.argv) > 1 and sys.argv[1] == "genkey":
        sys.argv[1] = "--generate-key"

    parser = argparse.ArgumentParser(
        description="CryptoClipboard Python CLI - Encrypt and decrypt clipboard content using Fernet.",
        epilog="Keyboard Shortcuts (when running):\n"
               "  Ctrl + Shift + E : Encrypt clipboard\n"
               "  Ctrl + Shift + D : Decrypt clipboard\n"
               "  Ctrl + Shift + K : Generate new key\n"
               "  Ctrl + Shift + I : Load key from clipboard",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--generate-key', '-g', action='store_true', help="Generate a new Fernet key, copy it, and exit.")
    parser.add_argument('--key', '-k', type=str, help="Specify a custom 32-byte Base64 Fernet key to use.")

    args = parser.parse_args()

    if args.generate_key:
        generate_new_key()
        return

    # Key Precedence: CLI argument > Env Var > Default Key
    initial_key = args.key or os.environ.get("CRYPTO_CLIPBOARD_KEY") or DEFAULT_KEY

    if not set_active_key(initial_key):
        print("⚠️ Warning: Provided Fernet key is invalid. Please supply a valid 32-byte Base64 key.")
        # Generate sample valid key to assist user
        sample = Fernet.generate_key().decode('utf-8')
        print(f"Example of a valid key: {sample}")
        return

    active = get_active_key()
    print("🔒 CryptoClipboard is running!")
    print("⌨️  Active Keyboard Shortcuts:")
    print("   - Ctrl + Shift + E : Encrypt text currently in clipboard")
    print("   - Ctrl + Shift + D : Decrypt text currently in clipboard")
    print("   - Ctrl + Shift + K : Generate new Fernet key and copy to clipboard")
    print("   - Ctrl + Shift + I : Load key from clipboard into CryptoClipboard")
    print("👁️  Automatic Clipboard Monitor: ACTIVE (auto-decrypts in console)")
    print(f"🔑 Active Key: {active[:8]}...")
    print("-" * 50)

    # 1. Start Background Clipboard Monitor
    start_clipboard_monitor()

    # 2. Start Global Keyboard Listener
    if KEYBOARD_AVAILABLE:
        try:
            # Register both lowercase and uppercase variations to ensure cross-platform pynput compatibility
            hotkey_map = {
                '<ctrl>+<shift>+e': encrypt_text,
                '<ctrl>+<shift>+d': decrypt_text,
                '<ctrl>+<shift>+k': generate_new_key,
                '<ctrl>+<shift>+i': load_key_from_clipboard,
                '<ctrl>+<shift>+E': encrypt_text,
                '<ctrl>+<shift>+D': decrypt_text,
                '<ctrl>+<shift>+K': generate_new_key,
                '<ctrl>+<shift>+I': load_key_from_clipboard,
            }
            hotkeys = keyboard.GlobalHotKeys(hotkey_map)
            hotkeys.daemon = True
            hotkeys.start()
            print("⌨️  Global keyboard listener started.")
        except Exception as e:
            print(f"⚠️ Could not start global keyboard listener: {e}")
    else:
        print("⚠️ Global keyboard listener unavailable. (pynput not installed)")

    # 3. Start System Tray Icon (Blocks main thread)
    run_tray()

if __name__ == "__main__":
    main()
