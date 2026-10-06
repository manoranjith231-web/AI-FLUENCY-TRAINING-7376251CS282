"""
Helper module for server management and health checks.
Ensures that the local Ollama emulation server is running before clients execute requests.
"""

import os
import sys
import time
import subprocess
import requests

SERVER_URL = "http://127.0.0.1:11434"


def is_server_running(timeout: float = 1.0) -> bool:
    """Checks if the Ollama service on 127.0.0.1:11434 is responding."""
    try:
        r = requests.get(f"{SERVER_URL}/api/version", timeout=timeout)
        if r.status_code == 200:
            return True
    except Exception:
        pass

    try:
        r = requests.get(f"{SERVER_URL}/", timeout=timeout)
        if r.status_code == 200:
            return True
    except Exception:
        pass

    return False


def ensure_server_running(timeout: float = 8.0) -> bool:
    """
    Checks if Ollama server is running; if not, automatically launches
    ollama_server.py as a background process and waits until ready.
    """
    if is_server_running(0.6):
        return True

    print("[*] Local Ollama server is not running on port 11434.")
    print("[*] Auto-starting 'ollama_server.py' in background...")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_script = os.path.join(script_dir, "ollama_server.py")

    if not os.path.exists(server_script):
        print(f"[!] Server script not found at {server_script}")
        return False

    creationflags = 0
    if sys.platform == "win32":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS

    try:
        subprocess.Popen(
            [sys.executable, server_script],
            cwd=script_dir,
            creationflags=creationflags,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=(sys.platform != "win32")
        )
    except Exception as e:
        print(f"[!] Failed to auto-start ollama_server.py: {e}")
        return False

    # Poll until ready
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(0.5)
        if is_server_running(0.5):
            print("[+] Ollama server started successfully on http://127.0.0.1:11434\n")
            return True

    print("[!] Timed out waiting for Ollama server to initialize.")
    print("    Please start the server manually in a separate terminal: python ollama_server.py\n")
    return False
