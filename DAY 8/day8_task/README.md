# Day 8 – Extend the College Helpdesk Agent

This project demonstrates RAG document ingestion, retrieval, tool calling, attendance eligibility validation, a relevance guard, and conversation memory.

## Important note about the starter data
The task sheet expects the six documents from your existing lab, including its original handbook and fee rules. This ZIP contains sample Markdown documents so the code can be explored as a complete starter project. If your instructor supplied five original lab documents, replace the corresponding sample files with those originals and keep the exact `placement_policy.md` required by the task sheet. Confirm the fee policy matches your lab instructions.

## Project files

- `lc_config.py`: model, embedding, and vector-store configuration
- `1_ingest.py`: loads Markdown documents and creates the Chroma index
- `2_search.py`: prints retrieval sources and similarity distances
- `task_agent.py`: agent tools, relevance guard, and five test questions
- `data/`: six Markdown documents
- `results.md`: report template
- `run_log.txt`: created from the actual terminal output

## Setup (Windows PowerShell)

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install packages:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Create `.env` from `.env.example` and add your own Groq API key:

   ```powershell
   Copy-Item .env.example .env
   ```

4. Ingest documents:

   ```powershell
   python 1_ingest.py
   ```

5. Inspect similarity scores:

   ```powershell
   python 2_search.py
   ```

6. Run the agent:

   ```powershell
   python task_agent.py
   ```

7. Save the terminal output:

   ```powershell
   python task_agent.py > run_log.txt 2>&1
   ```

Run `python task_agent.py` directly first to see any errors before redirecting output to the log file.

## Threshold tuning

`MAX_DISTANCE` defaults to `0.6`. The score scale depends on the embedding model and vector-store distance metric. Use measured results from `python 2_search.py`; choose a value that retains relevant placement results and rejects the France query. Set it in `.env` after testing.

## Git safety

Do not commit `.env`, `.venv/`, `chroma_db/`, or API keys. The `.gitignore` file excludes them.

## Results

Complete `results.md` with actual tool calls, answers, similarity scores, model names, and honest correctness assessments.
