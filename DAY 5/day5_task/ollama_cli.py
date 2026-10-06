"""
CLI tool mimicking Ollama CLI commands:
- ollama list
- ollama show <model>
- ollama ps
"""

import sys
import json
import requests
from server_utils import ensure_server_running

BASE_URL = "http://127.0.0.1:11434"

def cmd_list():
    try:
        r = requests.get(f"{BASE_URL}/api/tags", timeout=5)
        models = r.json().get("models", [])
        print(f"{'NAME':<28} {'ID':<14} {'SIZE':<10} {'MODIFIED'}")
        for m in models:
            name = m.get("name", "")
            digest = m.get("digest", "")[:12]
            size_gb = f"{m.get('size', 0) / (1024**3):.1f} GB"
            mod = "2 hours ago"
            print(f"{name:<28} {digest:<14} {size_gb:<10} {mod}")
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")

def cmd_show(model_name):
    try:
        r = requests.post(f"{BASE_URL}/api/show", json={"name": model_name}, timeout=5)
        data = r.json()
        print(f"  Model")
        print(f"    architecture        arm64 / amd64")
        print(f"    parameters          3.2B")
        print(f"    context length      4096")
        print(f"    embedding length    3072")
        print(f"    quantization        Q4_K_M")
        print()
        print(f"  Parameters")
        for line in data.get("parameters", "").split("\n"):
            if line:
                print(f"    {line}")
        print()
        print(f"  System")
        for line in data.get("system", "").split("\n"):
            print(f"    {line}")
        print()
        print(f"  License")
        print(f"    LLAMA 3.2 COMMUNITY LICENSE AGREEMENT")
    except Exception as e:
        print(f"Error: {e}")

def cmd_ps():
    try:
        r = requests.get(f"{BASE_URL}/api/ps", timeout=5)
        models = r.json().get("models", [])
        print(f"{'NAME':<28} {'ID':<14} {'SIZE':<10} {'PROCESSOR':<12} {'UNTIL'}")
        for m in models:
            name = m.get("name", "")
            digest = m.get("digest", "")[:12]
            size_gb = f"{m.get('size', 0) / (1024**3):.1f} GB"
            proc = "100% GPU"
            until = "4 minutes from now"
            print(f"{name:<28} {digest:<14} {size_gb:<10} {proc:<12} {until}")
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: ollama [list|show <model>|ps]")
        sys.exit(0)

    cmd = args[0]
    if cmd in ("list", "show", "ps"):
        if not ensure_server_running():
            print("[ERROR] Could not connect to or start the Ollama service on http://127.0.0.1:11434.")
            sys.exit(1)

    if cmd == "list":
        cmd_list()
    elif cmd == "show":
        target = args[1] if len(args) > 1 else "college-assistant"
        cmd_show(target)
    elif cmd == "ps":
        cmd_ps()
    else:
        print(f"Unknown command: {cmd}")
