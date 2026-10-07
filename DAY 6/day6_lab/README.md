# Day 6 – Robust Agents and Structured Outputs

## Overview

Day 6 focuses on making AI agents more reliable, safe, and predictable.

In earlier agent implementations, the model could generate incorrect tool arguments, invalid JSON, unknown tools, or unsafe expressions. A robust agent should not blindly execute these requests.

This project improves the agent by adding:

- Tool argument validation
- Strict JSON Schema validation
- Safe tool execution
- Error handling
- Retry and recovery logic
- Protection against repeated tool calls
- Safe arithmetic evaluation
- Structured JSON outputs
- Fault injection testing

The project uses the **Groq API** with the `openai/gpt-oss-20b` model.

---

## Objectives

The main objectives of Day 6 are:

1. Validate tool arguments before execution.
2. Prevent invalid JSON from crashing the agent.
3. Reject unknown tools.
4. Detect missing required arguments.
5. Reject incorrect argument types.
6. Reject invalid enum values.
7. Reject invented or extra arguments.
8. Safely handle tool execution errors.
9. Prevent unsafe calculator expressions.
10. Build structured JSON responses using a JSON Schema.
11. Test the robustness of the agent using fault injection.
12. Build an agent that can recover from tool errors instead of crashing.

---

## Project Structure

```text
Day_6/
│
├── README.md
├── analysis.md
│
├── robust_agent.py
├── tools_v2.py
├── validate.py
├── structured_demo.py
├── inject_faults.py
│
├── requirements.txt
├── .env
└── .gitignore