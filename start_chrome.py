"""
Start Chrome with Remote Debugging

Run this script ONCE to start Chrome with remote debugging enabled.
Then you can run main.py multiple times without closing Chrome.

Your MEXC login will persist since it uses your Chrome profile.
"""

import subprocess
import os
import sys
import time

# Configuration - UPDATE THESE TO MATCH YOUR SYSTEM
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

PROFILE_PATH = r"C:\Users\osama.ahmed\AppData\Local\Google\Chrome\User Data"
PROFILE_NAME = "Profile 2"
DEBUGGING_PORT = 9222


def find_chrome():
    for path in CHROME_PATHS:
        if os.path.exists(path):
            return path
    return None


def is_chrome_running_with_debug():
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', DEBUGGING_PORT)) == 0


def main():
    print("=" * 50)
    print("  Chrome Remote Debugging Launcher")
    print("=" * 50)
    
    # Check if already running
    if is_chrome_running_with_debug():
        print(f"\n✓ Chrome is already running with debugging on port {DEBUGGING_PORT}")
        print("  You can now run: python main.py")
        return
    
    # Find Chrome
    chrome_path = find_chrome()
    if not chrome_path:
        print("\n✗ Chrome not found! Please update CHROME_PATHS in this script.")
        sys.exit(1)
    
    print(f"\nChrome found at: {chrome_path}")
    print(f"Profile path: {PROFILE_PATH}")
    print(f"Profile name: {PROFILE_NAME}")
    print(f"Debug port: {DEBUGGING_PORT}")
    
    # Check if profile path exists
    if not os.path.exists(PROFILE_PATH):
        print(f"\n⚠ Warning: Profile path does not exist: {PROFILE_PATH}")
        print("  Please update PROFILE_PATH in this script.")
        resp = input("Continue anyway? (y/n): ")
        if resp.lower() != 'y':
            sys.exit(1)
    
    print("\n[*] Starting Chrome with remote debugging...")
    print("    IMPORTANT: Close ALL existing Chrome windows first!")
    
    input("\nPress Enter when you've closed all Chrome windows...")
    
    # Build command
    cmd = [
        chrome_path,
        f"--remote-debugging-port={DEBUGGING_PORT}",
        f"--user-data-dir={PROFILE_PATH}",
        f"--profile-directory={PROFILE_NAME}",
        "--start-maximized",
    ]
    
    try:
        subprocess.Popen(cmd)
        print("\n✓ Chrome started successfully!")
        
        # Wait for Chrome to start
        time.sleep(3)
        
        if is_chrome_running_with_debug():
            print(f"✓ Remote debugging active on port {DEBUGGING_PORT}")
            print("\n" + "=" * 50)
            print("  You can now run: python main.py")
            print("  Chrome will stay open between trades!")
            print("=" * 50)
        else:
            print("⚠ Chrome started but debugging port not detected.")
            print("  The bot may still work, try running: python main.py")
            
    except Exception as e:
        print(f"\n✗ Failed to start Chrome: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()