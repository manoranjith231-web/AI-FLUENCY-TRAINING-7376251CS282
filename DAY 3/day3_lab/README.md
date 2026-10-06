# Day 3 – Build a ReAct Agent from Scratch, Break It on Purpose, Then Fix It

## 1. Project Overview

This project is part of the Agentic AI: Foundations and Open-Source Practice – Day 3 Lab.

The objective is to build a ReAct agent from scratch using plain Python. The agent uses two tools:

1. `calculator()` – safely performs arithmetic calculations.
2. `read_webpage()` – reads a local HTML/text file or a web page and returns readable text.

The agent follows the ReAct cycle:

**Reason → Act → Observe → Repeat/Stop**

The project also deliberately triggers three failure modes:

* Repeating tool-call loop
* Hallucinated/unknown tool call
* Context overflow and runaway cost

After observing these failures, guards are added to make the agent safer and more reliable.

---

## 2. Objectives

The main objectives of this lab are:

* Create a tool registry.
* Create JSON schemas for tools.
* Build a ReAct agent loop.
* Read local HTML/text files.
* Perform calculations using information obtained from a document.
* Handle tool errors without crashing.
* Detect repeated tool calls.
* Limit tool output size.
* Add a character budget.
* Compare the unguarded and guarded agent.

---

## 3. Project Structure

```text
day3_task/
│
├── config.py
├── check_setup.py
├── notice.html
├── my_tools.py
├── my_agent.py
├── my_agent_fixed.py
├── big.html
├── README.md
├── analysis.md
│
└── screenshots/
    ├── 01_my_tools.png
    ├── 02_agent_basic.png
    ├── 03_hostel_question.png
    ├── 04_no_tool_needed.png
    ├── 05_failure_repeating_loop.png
    ├── 06_failure_unknown_tool.png
    ├── 06b_failure_keyerror.png
    ├── 07_failure_context_overflow.png
    └── 08_agent_fixed.png
```

The lab manual identifies `my_tools.py`, `my_agent.py`, and `my_agent_fixed.py` as the main program files and requires a failure log and observation table.

---

## 4. Requirements

### Software

* Python
* Visual Studio Code
* Python virtual environment
* LLM provider such as Ollama, Groq, or Hugging Face
* `requests` package for real web URLs

Install requests:

```bash
pip install requests
```

Local HTML/text files can be used without internet access.

---

## 5. Notice File

The agent reads information from `notice.html`.

The file contains:

| Course |        Fee |
| ------ | ---------: |
| CS101  | Rs. 12,000 |
| AI202  | Rs. 18,000 |
| DS303  | Rs. 15,000 |

Additional information:

* Merit scholarship gives a 10% reduction on the total fee.
* Hostel students pay Rs. 4,500 additional laboratory charges.
* Script/style content should not appear in the tool output.

---

## 6. Tools

### Calculator

The calculator safely evaluates arithmetic expressions without using `eval()`.

Example:

```text
(12000 + 18000) * 0.9
```

Result:

```text
27000.0
```

The calculator accepts supported arithmetic operations and returns an error message for invalid expressions.

### Web Page Reader

`read_webpage()` can read:

* Local HTML files
* Local text files
* HTTP/HTTPS web pages

It removes HTML tags and script/style content and limits the output to prevent excessive context.

---

## 7. Basic Tool Test

Run:

```bash
python my_tools.py
```

Expected important outputs include:

```text
27000.0
1024
Calculator error: ...
Fee Notice Department of AI and Data Science ...
Read error: 'no_such_file.html' is not a URL and no such file exists.
```

The tool test also demonstrates that `import os` is rejected and that script content is removed from the webpage output.

---

## 8. ReAct Agent

The basic agent is implemented in:

```text
my_agent.py
```

The agent performs six main operations:

1. Reason
2. Stop if no tool is required
3. Record the tool request
4. Act using the selected tool
5. Observe the tool result
6. Stop when the maximum step limit is reached

The basic agent uses `TOOL_FUNCTIONS.get(name)` so an unknown tool can be returned as an error instead of immediately crashing the program.

---

## 9. Basic Test

Question:

```text
Read notice.html and tell me the total fee for CS101 and AI202 after the merit scholarship.
```

Expected calculation:

```text
(12000 + 18000) × 0.9
= 27000
```

Expected answer:

```text
The total fee after the 10 percent merit scholarship is Rs. 27,000.
```

The expected trace contains a `read_webpage` call followed by a `calculator` call.

---

## 10. Additional Agent Tests

### Test 1 – Hostel Student

Question:

```text
Read notice.html. What does a hostel student taking all three courses pay in total, including laboratory charges?
```

Expected calculation:

```text
12000 + 18000 + 15000 = 45000
45000 + 4500 = 49500
```

Expected total:

```text
Rs. 49,500
```

### Test 2 – Percentage

Question:

```text
What is 15% of the AI202 fee?
```

AI202 fee:

```text
Rs. 18,000
```

Calculation:

```text
18000 × 0.15 = 2700
```

Expected answer:

```text
Rs. 2,700
```

### Test 3 – No Tool Required

Question:

```text
Write a one-line welcome message for new students.
```

Expected behavior:

```text
No tool call.
```

The agent should answer directly.

---

## 11. Failure Testing

### Failure 1 – Repeating Loop

Question:

```text
Read fees.html and tell me the fee for CS101.
```

`fees.html` does not exist.

The model may repeatedly call:

```text
read_webpage('fees.html')
```

until the maximum step limit is reached.

This demonstrates a repeating loop.

---

### Failure 2 – Unknown Tool

The system prompt is temporarily changed to mention:

```text
send_email
```

even though this tool is not registered.

The safe registry lookup:

```python
TOOL_FUNCTIONS.get(name)
```

returns an unknown-tool message instead of crashing.

If the lookup is changed to:

```python
TOOL_FUNCTIONS[name]
```

the program can crash with a `KeyError`.

The unsafe version is used only for the experiment and must be changed back afterward.

---

### Failure 3 – Context Overflow

A large `big.html` file is created with thousands of student records.

The normal `max_chars=2000` protection is temporarily removed.

Possible outcomes include:

* Context-length error
* Very long processing time
* Rate-limit error
* Agent forgetting the original question

After the experiment, `max_chars` must be restored to 2000.

---

## 12. Fixed Agent

The fixed version is:

```text
my_agent_fixed.py
```

It adds three important guards:

### 1. Repeat Detection

The agent tracks identical tool calls.

After the third identical call, the agent stops.

### 2. Observation Truncation

Each tool result is limited to:

```text
1500 characters
```

### 3. Character Budget

The total character budget is:

```text
30000 characters
```

These guards reduce repeated calls, excessive context, and runaway processing.

Run:

```bash
python my_agent_fixed.py
```

The program tests:

1. Normal scholarship question
2. Missing `fees.html`
3. Large `big.html`

The expected behavior is that the missing-file question stops after the repeat threshold instead of consuming all six steps.

---

## 13. Conclusion

This lab demonstrates how a ReAct agent can use tools to read information and perform calculations.

The unguarded agent can experience:

* Repeating loops
* Unknown tool calls
* Context overflow

The fixed agent uses:

* Repeat detection
* Output truncation
* Character-budget protection

The experiment shows that tool safety and stopping conditions are important when building reliable AI agents.
