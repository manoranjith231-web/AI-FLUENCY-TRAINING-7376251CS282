"""
Day 5: Ollama REST API Benchmark Script
Calls http://localhost:11434/api/generate directly using `requests`:
1. Non-streaming request -> measures Total Time, Generated Tokens, Tokens/Second
2. Streaming request -> measures Time to First Token (TTFT), Total Time, Generated Tokens, Tokens/Second
"""

import sys
import time
import json
import requests
from server_utils import ensure_server_running

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

OLLAMA_URL = "http://127.0.0.1:11434"
MODEL = "college-assistant"


def non_streaming_request(prompt: str):
    """Executes a single non-streaming POST request to /api/generate."""
    url = f"{OLLAMA_URL}/api/generate"
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    print("\n" + "=" * 65)
    print("1. NON-STREAMING REQUEST (/api/generate)")
    print("=" * 65)
    print(f"Prompt: {prompt}\n")

    start_time = time.perf_counter()
    response = requests.post(url, json=payload, timeout=120)
    end_time = time.perf_counter()

    response.raise_for_status()
    result = response.json()

    answer = result.get("response", "")
    total_time = end_time - start_time
    eval_count = result.get("eval_count", 0)
    eval_duration = result.get("eval_duration", 0)

    if eval_duration > 0:
        tokens_per_second = eval_count / (eval_duration / 1_000_000_000)
    elif total_time > 0:
        tokens_per_second = eval_count / total_time
    else:
        tokens_per_second = 0.0

    print("Response:")
    print(answer.strip())

    print("\n" + "-" * 40)
    print("PERFORMANCE TELEMETRY")
    print("-" * 40)
    print(f"Total time elapsed : {total_time:.3f} s")
    print(f"Generated tokens   : {eval_count} tokens")
    print(f"Throughput         : {tokens_per_second:.2f} tokens/s")
    print("-" * 40)
    return {"total_time": total_time, "eval_count": eval_count, "tokens_per_second": tokens_per_second}


def streaming_request(prompt: str):
    """Executes a streaming POST request to /api/generate and measures TTFT."""
    url = f"{OLLAMA_URL}/api/generate"
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": True
    }

    print("\n" + "=" * 65)
    print("2. STREAMING REQUEST (/api/generate)")
    print("=" * 65)
    print(f"Prompt: {prompt}\n")
    print("Response (Streaming Tokens):")

    start_time = time.perf_counter()
    first_token_time = None
    final_result = {}

    response = requests.post(url, json=payload, stream=True, timeout=120)
    response.raise_for_status()

    for line in response.iter_lines():
        if not line:
            continue
        try:
            chunk = json.loads(line.decode("utf-8"))
            token = chunk.get("response", "")

            if token:
                if first_token_time is None:
                    first_token_time = time.perf_counter()
                print(token, end="", flush=True)

            if chunk.get("done"):
                final_result = chunk
        except Exception:
            pass

    end_time = time.perf_counter()
    print("\n")

    ttft = (first_token_time - start_time) if first_token_time else 0.0
    total_time = end_time - start_time
    eval_count = final_result.get("eval_count", 0)
    eval_duration = final_result.get("eval_duration", 0)

    if eval_duration > 0:
        tokens_per_second = eval_count / (eval_duration / 1_000_000_000)
    elif total_time > 0:
        tokens_per_second = eval_count / total_time
    else:
        tokens_per_second = 0.0

    print("-" * 40)
    print("STREAMING PERFORMANCE METRICS")
    print("-" * 40)
    print(f"Time to First Token (TTFT) : {ttft:.3f} s")
    print(f"Total time elapsed         : {total_time:.3f} s")
    print(f"Generated tokens           : {eval_count} tokens")
    print(f"Throughput                 : {tokens_per_second:.2f} tokens/s")
    print("-" * 40)
    return {"ttft": ttft, "total_time": total_time, "eval_count": eval_count, "tokens_per_second": tokens_per_second}


if __name__ == "__main__":
    print("=" * 65)
    print("   DAY 5 - OLLAMA REST API BENCHMARK")
    print(f"   Model  : {MODEL}")
    print(f"   Server : {OLLAMA_URL}")
    print("=" * 65)

    if not ensure_server_running():
        print("[ERROR] Cannot connect to Ollama server on http://127.0.0.1:11434.")
        print("Please start the server first with: python ollama_server.py")
        sys.exit(1)

    prompt_non_stream = "What is the recommended study approach for mastering Object-Oriented Programming in C++?"
    non_streaming_request(prompt_non_stream)

    prompt_stream = "Explain time complexity and Big-O notation simply for a 1st year engineering student."
    streaming_request(prompt_stream)

    print("\n" + "=" * 65)
    print("OLLAMA REST API BENCHMARK COMPLETED SUCCESSFULLY")
    print("=" * 65)
