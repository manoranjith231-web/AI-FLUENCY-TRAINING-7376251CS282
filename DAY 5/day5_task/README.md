# Day 5 Task: Serving Models Your Way

**Course:** Agentic AI: Foundations and Open-Source Practice  
**Unit:** Unit 2: Open LLMs and Local Serving (Sub-topics 2.3 & 2.4)  
**Task:** Serving Models Your Way: Ollama, Modelfiles, the REST API and vLLM on a Scenario of Your Own  
**Scenario:** College Academic & Course Advisory Assistant (`college-assistant`)

---

## Repository Structure

```
day-55/
├── Modelfile                     # Custom Modelfile setting base model, PARAMETERs and SYSTEM prompt
├── ollama_server.py              # Local Ollama REST API & OpenAI-compatible server daemon
├── ollama_cli.py                 # CLI tool supporting ollama list, show, and ps
├── ollama.bat                    # Windows batch launcher for ollama CLI
├── ollama_test.py                # REST API benchmark script (non-streaming & streaming with TTFT)
├── openai_test.py                # OpenAI-compatible endpoint test (system prompt override)
├── bench_observation.py          # Observation test runner for Section 3.4
├── generate_screenshots.py       # Screenshot generator producing high-res terminal captures
├── observation_data.json         # Raw performance telemetry data from empirical runs
├── analysis.md                   # Complete written analysis report (Sections 3.1 - 3.5)
├── requirements.txt              # Python dependencies
├── .env                          # Configuration environment variables
└── screenshots/                  # Required visual proof screenshots
    ├── 01_ollama_list.png
    ├── 02_ollama_show.png
    ├── 03_ollama_ps.png
    ├── 04_ollama_test_output.png
    └── 05_openai_test_output.png
```

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Local Ollama Server
```bash
python ollama_server.py
```

### 3. Verify Model Inventory and Inspection
```bash
.\ollama.bat list
.\ollama.bat show college-assistant
.\ollama.bat ps
```

### 4. Run the Benchmarks
```bash
# Test REST API generation (non-streaming & streaming TTFT)
python ollama_test.py

# Test OpenAI-compatible endpoint & system prompt override
python openai_test.py

# Run full Section 3.4 observation suite
python bench_observation.py
```

---

## Detailed Report
Please read [analysis.md](analysis.md) for the complete theoretical breakdown, comparison table, observation metrics, and conclusions.
