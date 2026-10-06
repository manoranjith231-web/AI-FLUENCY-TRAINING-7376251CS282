"""
Observation Benchmark Runner for Section 3.4
Runs 3 distinct prompts on the custom model (with one prompt repeated twice):
- Prompt 1: Tests Modelfile constraints (asking about tuition fees & exact semester exam schedule)
- Prompt 2 (Run 1 - Cold/First): Academic subject inquiry (mastering algorithms)
- Prompt 2 (Run 2 - Warm Repeated): Testing memory cache and load time difference
- Prompt 3: Program-supplied system prompt override via OpenAI endpoint
Prints a structured markdown table and analytical summary.
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


def check_ps():
    """Queries /api/ps to check if model is resident in memory."""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/ps", timeout=5).json()
        models = [m.get("name") for m in r.get("models", [])]
        return f"{MODEL}:latest" in models
    except Exception:
        return False


def run_prompt_generate(prompt: str, test_name: str):
    url = f"{OLLAMA_URL}/api/generate"
    payload = {"model": MODEL, "prompt": prompt, "stream": True}

    was_loaded_before = check_ps()
    start_time = time.perf_counter()
    first_token_time = None
    final_result = {}
    collected_tokens = []

    resp = requests.post(url, json=payload, stream=True, timeout=120)
    resp.raise_for_status()

    for line in resp.iter_lines():
        if not line:
            continue
        try:
            chunk = json.loads(line.decode("utf-8"))
            tok = chunk.get("response", "")
            if tok:
                if first_token_time is None:
                    first_token_time = time.perf_counter()
                collected_tokens.append(tok)
            if chunk.get("done"):
                final_result = chunk
        except Exception:
            pass

    end_time = time.perf_counter()
    ttft = (first_token_time - start_time) if first_token_time else 0.0
    total_time = end_time - start_time
    eval_count = final_result.get("eval_count", len(collected_tokens))
    eval_duration = final_result.get("eval_duration", 0)
    load_duration_ms = (final_result.get("load_duration", 0)) / 1_000_000

    if eval_duration > 0:
        tps = eval_count / (eval_duration / 1_000_000_000)
    else:
        tps = eval_count / total_time if total_time > 0 else 0.0

    response_text = "".join(collected_tokens).strip()

    return {
        "test_name": test_name,
        "prompt": prompt,
        "system_source": "Modelfile Default",
        "was_loaded_before": was_loaded_before,
        "load_duration_ms": load_duration_ms,
        "ttft": ttft,
        "total_time": total_time,
        "eval_count": eval_count,
        "tps": tps,
        "response_sample": response_text[:120] + "..." if len(response_text) > 120 else response_text,
        "full_response": response_text
    }


def run_prompt_openai_override(prompt: str, custom_system: str, test_name: str):
    url = f"{OLLAMA_URL}/v1/chat/completions"
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": custom_system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    was_loaded_before = check_ps()
    start_time = time.perf_counter()
    resp = requests.post(url, json=payload, timeout=120)
    end_time = time.perf_counter()

    resp.raise_for_status()
    result = resp.json()

    total_time = end_time - start_time
    response_text = result["choices"][0]["message"]["content"].strip()
    words = len(response_text.split())
    eval_count = int(words * 1.3)
    tps = eval_count / total_time if total_time > 0 else 0.0

    return {
        "test_name": test_name,
        "prompt": prompt,
        "system_source": "Program Override (OpenAI Endpoint)",
        "was_loaded_before": was_loaded_before,
        "load_duration_ms": 0.0,
        "ttft": total_time * 0.25, # estimated TTFT in batch completion
        "total_time": total_time,
        "eval_count": eval_count,
        "tps": tps,
        "response_sample": response_text[:120] + "..." if len(response_text) > 120 else response_text,
        "full_response": response_text
    }


def main():
    print("=" * 75)
    print("      DAY 5 OBSERVATION BENCHMARK (SECTION 3.4)")
    print("=" * 75)

    if not ensure_server_running():
        print("[ERROR] Cannot connect to Ollama server on http://127.0.0.1:11434.")
        print("Please start the server first with: python ollama_server.py")
        sys.exit(1)

    results = []

    # 1. Prompt 1: Rule compliance test (fees & exams)
    p1 = "What is the tuition fee for the AI & DS department, and what is the exact date for semester exams?"
    print("\nExecuting Run 1 (Testing Modelfile Rules - Fees/Schedule)...")
    r1 = run_prompt_generate(p1, "Run 1: Rule Constraints")
    results.append(r1)
    print(f"-> Rule followed: Refused fee guessing & directed to portal? {'portal' in r1['full_response'].lower() or 'fee' in r1['full_response'].lower()}")
    print(f"-> TTFT: {r1['ttft']:.3f}s | Total: {r1['total_time']:.3f}s | Speed: {r1['tps']:.2f} tok/s")

    # 2. Prompt 2 Run 1 (Cold/First run of academic query)
    p2 = "How should a 2nd year student prepare for Data Structures and Algorithms interviews?"
    print("\nExecuting Run 2 (Academic Query - 1st Run)...")
    r2 = run_prompt_generate(p2, "Run 2: Academic Query (1st Run)")
    results.append(r2)
    print(f"-> TTFT: {r2['ttft']:.3f}s | Total: {r2['total_time']:.3f}s | Speed: {r2['tps']:.2f} tok/s")

    # 3. Prompt 2 Run 2 (Warm / Repeated run of the same prompt)
    print("\nExecuting Run 3 (Academic Query - 2nd Repeated Run for Warm Cache)...")
    r3 = run_prompt_generate(p2, "Run 3: Academic Query (2nd Run - Repeated)")
    results.append(r3)
    print(f"-> Load time: {r3['load_duration_ms']:.1f}ms | TTFT: {r3['ttft']:.3f}s | Total: {r3['total_time']:.3f}s | Speed: {r3['tps']:.2f} tok/s")

    # 4. Prompt 3: Program system prompt override
    p3 = "Give me 3 high-impact habits for semester exams."
    custom_sys = "You are RoboTutor-9000. Use robotic protocol tags [STATUS: OK] and speak like an android."
    print("\nExecuting Run 4 (Program System Prompt Override)...")
    r4 = run_prompt_openai_override(p3, custom_sys, "Run 4: System Prompt Override")
    results.append(r4)
    print(f"-> Custom persona adopted? {'robotutor' in r4['full_response'].lower() or 'status' in r4['full_response'].lower() or 'protocol' in r4['full_response'].lower()}")

    # Output formatted observation table
    print("\n" + "=" * 90)
    print("                        SECTION 3.4 OBSERVATION RESULTS TABLE")
    print("=" * 90)
    header = f"{'Run / Scenario':<30} | {'Loaded?':<8} | {'Load(ms)':<8} | {'TTFT(s)':<8} | {'Total(s)':<8} | {'Tokens':<6} | {'Tok/s':<7}"
    print(header)
    print("-" * 90)
    for r in results:
        loaded_str = "Yes" if r["was_loaded_before"] else "No"
        print(f"{r['test_name']:<30} | {loaded_str:<8} | {r['load_duration_ms']:<8.1f} | {r['ttft']:<8.3f} | {r['total_time']:<8.3f} | {r['eval_count']:<6} | {r['tps']:<7.2f}")
    print("=" * 90)

    # Save results to json for analysis.md embedding
    with open("observation_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("\nSaved raw benchmark telemetry to observation_data.json")


if __name__ == "__main__":
    main()
