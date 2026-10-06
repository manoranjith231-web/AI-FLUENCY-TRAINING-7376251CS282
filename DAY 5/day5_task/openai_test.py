"""
Day 5: OpenAI-Compatible Endpoint Test
Calls http://localhost:11434/v1/chat/completions
Supplies a custom programmatic system prompt to demonstrate whether the Modelfile default
or the program's runtime prompt takes precedence ("which one wins?").
"""

import sys
import time
import requests
from server_utils import ensure_server_running

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

OLLAMA_OPENAI_URL = "http://127.0.0.1:11434/v1/chat/completions"
MODEL = "college-assistant"


def test_openai_override():
    print("=" * 65)
    print("   DAY 5 - OLLAMA OPENAI-COMPATIBLE ENDPOINT TEST")
    print(f"   Endpoint : {OLLAMA_OPENAI_URL}")
    print(f"   Model    : {MODEL}")
    print("=" * 65)

    if not ensure_server_running():
        print("[ERROR] Cannot connect to Ollama server on http://127.0.0.1:11434.")
        print("Please start the server first with: python ollama_server.py")
        sys.exit(1)

    # We provide a strict programmatic system prompt with a radically different persona:
    # A futuristic robotic AI with robotic tone markers.
    program_system_prompt = (
        "You are UNIT-702, an ultra-strict cybernetic examination bot. "
        "Begin every response with '[SYSTEM PROTOCOL ACTIVE]'. "
        "Speak in formal, robotic, direct language without pleasantries. "
        "Conclude with '[TRANSMISSION TERMINATED]'."
    )

    user_query = "What are the rules regarding missed internal assessment exams?"

    messages = [
        {"role": "system", "content": program_system_prompt},
        {"role": "user", "content": user_query}
    ]

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.2
    }

    print("\nProgram-Supplied System Prompt:")
    print(f'"{program_system_prompt}"')
    print(f"\nUser Query: {user_query}")
    print("\nSubmitting request to /v1/chat/completions ...\n")

    start_time = time.perf_counter()
    response = requests.post(OLLAMA_OPENAI_URL, json=payload, timeout=120)
    end_time = time.perf_counter()

    response.raise_for_status()
    result = response.json()

    assistant_message = result["choices"][0]["message"]["content"]
    total_time = end_time - start_time

    print("-" * 65)
    print("ASSISTANT RESPONSE RECEIVED:")
    print("-" * 65)
    print(assistant_message.strip())
    print("-" * 65)

    print("\n" + "=" * 40)
    print("ANALYSIS: WHICH PROMPT WON?")
    print("=" * 40)
    if "[SYSTEM PROTOCOL ACTIVE]" in assistant_message or "UNIT-702" in assistant_message:
        print(">> RESULT: The PROGRAM'S system prompt WON!")
        print(">> The runtime system prompt successfully overrode the Modelfile default.")
    else:
        print(">> RESULT: The Modelfile system prompt was retained.")
    print(f">> Total response latency: {total_time:.3f} s")
    print("=" * 65)


if __name__ == "__main__":
    test_openai_override()
