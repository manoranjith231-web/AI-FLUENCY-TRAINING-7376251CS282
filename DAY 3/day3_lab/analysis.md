# Day 3 – Agent Failure Analysis and Observations

## 1. Introduction

The Day 3 lab focuses on building a ReAct agent with two tools:

* `calculator`
* `read_webpage`

The basic agent is intentionally created without all safety guards so that failure modes can be observed. After the failures are recorded, repeat detection, output truncation, and a character budget are added.

---

# 2. Tool Analysis

## 2.1 Calculator

The calculator uses Python AST parsing instead of `eval()`.

Example:

```text
(12000 + 18000) * 0.9
```

Output:

```text
27000.0
```

Invalid expressions such as:

```text
import os
```

are rejected.

### Why this is important

Using `eval()` could allow unwanted Python expressions to execute. The AST-based calculator accepts only the supported arithmetic operations.

---

## 2.2 Web Page Reader

The `read_webpage()` tool can read:

* Local HTML files
* Local text files
* HTTP/HTTPS pages

It removes HTML tags and removes script/style content.

The default output limit is:

```text
2000 characters
```

This prevents a large document from unnecessarily filling the model context.

---

# 3. Part C – Step Count Observations

| Question                |        Steps Used | Tools Called                 |
| ----------------------- | ----------------: | ---------------------------- |
| Merit scholarship total |                 2 | `read_webpage`, `calculator` |
| Hostel student total    | Record actual run | `read_webpage`, `calculator` |
| 15% of AI202            | Record actual run | `read_webpage`, `calculator` |
| Welcome message         |                 0 | None                         |

The lab manual expects one read and calculation for the percentage question and no tool call for the welcome message.

---

# 4. Failure 1 – Repeating Loop

## Test

```text
Read fees.html and tell me the fee for CS101.
```

The file `fees.html` does not exist.

The tool returns:

```text
Read error: 'fees.html' is not a URL and no such file exists.
```

The unguarded model may request the same tool call repeatedly.

Example:

```text
step 1: read_webpage({'url': 'fees.html'})
step 2: read_webpage({'url': 'fees.html'})
step 3: read_webpage({'url': 'fees.html'})
...
```

Eventually the maximum step limit stops the agent.

### Analysis

The model is not necessarily making a factual mistake. The problem is that the agent loop has no repeat-detection mechanism.

A better behavior would be to recognize that the same tool call has failed repeatedly and stop with a useful error message.

### Cost

```text
Steps used: Record actual run
Repeated calls: Record actual run
Time/cost: Record actual run
```

---

# 5. Failure 2 – Hallucinated Tool

## Test

The system prompt is temporarily changed to mention:

```text
send_email
```

However, the registered tools are only:

```text
calculator
read_webpage
```

The model may try to call:

```text
send_email
```

The safe registry lookup is:

```python
function = TOOL_FUNCTIONS.get(name)
```

This allows the program to return:

```text
Unknown tool: send_email
```

instead of crashing.

---

# 6. Unsafe Registry Test

The safe lookup:

```python
TOOL_FUNCTIONS.get(name)
```

is temporarily changed to:

```python
TOOL_FUNCTIONS[name]
```

If the model requests `send_email`, the dictionary does not contain that key.

Therefore Python raises:

```text
KeyError
```

### Analysis

The safe `.get()` method allows the program to handle an unexpected tool request gracefully.

The unsafe `[]` lookup causes the entire run to crash.

After completing the experiment, the safe version must be restored.

---

# 7. Failure 3 – Context Overflow

A large `big.html` file is created containing thousands of student records.

The normal:

```python
max_chars=2000
```

limit is temporarily increased to:

```python
max_chars=200000
```

This allows a very large amount of text to reach the model.

Possible results include:

* Context-length error
* Very long processing time
* Rate-limit error
* The agent losing track of the original question

The exact result should be recorded from the actual execution.

### My observation

```text
Observed result: ______________________________

Time taken: ___________________________________

Error/message: ________________________________
```

---

# 8. Failure Log

| Failure                      | What happened without guards                               | Cost                            |
| ---------------------------- | ---------------------------------------------------------- | ------------------------------- |
| Repeating loop               | Same missing-file tool call repeated                       | Record actual steps/time        |
| Unknown tool – safe `.get()` | Returned `Unknown tool` message                            | One tool call / normal handling |
| Unknown tool – unsafe `[]`   | Program crashed with `KeyError`                            | Run lost                        |
| Context overflow             | Large output caused one of the documented failure outcomes | Record actual result            |

The lab specifically asks for these four failure-log entries.

---

# 9. Fixes Added

## 9.1 Repeat Detection

The fixed agent stores:

```python
seen_calls = {}
```

Each tool call is represented by its tool name and arguments.

If the same call reaches the third occurrence, the agent stops.

Example:

```text
Stopped: the tool read_webpage was called 3 times with the same arguments and no progress was made.
```

### Purpose

Prevents the agent from wasting steps repeatedly requesting the same failed operation.

---

## 9.2 Observation Truncation

The fixed agent uses:

```python
MAX_TOOL_CHARS = 1500
```

If a tool returns more than 1500 characters, the result is shortened.

### Purpose

Prevents one large observation from flooding the model context.

---

## 9.3 Character Budget

The fixed agent uses:

```python
CHAR_BUDGET = 30000
```

If the amount of text sent to the model exceeds the budget, the agent stops.

### Purpose

Provides an additional protection against runaway context and cost.

---

# 10. After-Fix Observation

| Failure          | Behaviour with Guards                                                 | Guard Used                       |
| ---------------- | --------------------------------------------------------------------- | -------------------------------- |
| Repeating loop   | Stops after the same tool call is repeated 3 times                    | Repeat detection                 |
| Unknown tool     | Returns an `Unknown tool` message instead of crashing                 | Safe `.get()` registry           |
| Context overflow | Large observations are truncated and total character usage is limited | `MAX_TOOL_CHARS` + `CHAR_BUDGET` |

The fixed agent's documented expected behavior is to stop the missing-file question after three identical calls and protect the large-page question using truncation/budget controls.

---

# 11. Chosen Limits

| Setting          | Value | Justification                                                    |
| ---------------- | ----: | ---------------------------------------------------------------- |
| `max_steps`      |     6 | Provides enough steps for normal read + calculation tasks        |
| `MAX_TOOL_CHARS` |  1500 | Keeps individual observations reasonably small                   |
| `CHAR_BUDGET`    | 30000 | Allows normal agent runs while limiting excessive context        |
| Repeat threshold |     3 | Stops repeated failures while allowing legitimate repeated calls |

The lab manual recommends choosing `max_steps` based on the longest successful run and provides 1500, 30000, and 3 as the fixed-agent values/examples.

---

# 12. Comparison – Before and After

| Feature                 | Basic Agent                | Fixed Agent                            |
| ----------------------- | -------------------------- | -------------------------------------- |
| Repeated call detection | No                         | Yes                                    |
| Tool output limit       | Tool-level 2000 chars      | Additional 1500-char observation limit |
| Character budget        | No                         | Yes                                    |
| Unknown tool handling   | Safe `.get()`              | Safe `.get()`                          |
| Missing-file loop       | Can repeat until max steps | Stops after 3 identical calls          |
| Large page protection   | Basic tool truncation      | Tool truncation + agent guards         |

---

# 13. Discussion Answers

## 1. Whose fault is the repeating loop?

The loop is mainly a limitation of the agent's control logic. The model requested a file that the user asked it to read, but after receiving the same failure it continued requesting the same operation. The fix should therefore be placed in the agent loop through repeat detection.

## 2. Why is an Unknown Tool message better than a crash?

An agent should continue operating or provide a useful error message when a model requests an unavailable tool. A `KeyError` terminates the program and loses the complete run. Returning an error string allows the model to observe the failure and potentially respond appropriately.

## 3. What information can be lost by truncation?

Important information near the end of a document may be removed. A better design could provide summaries, pagination, search, or chunked reading so the agent can request the remaining content when necessary.

## 4. Why is a character budget useful?

The character budget is a simple approximation of resource usage. It is not a true token or monetary-cost measurement, but it still prevents an unexpectedly large amount of text from being repeatedly sent to the model.

## 5. Would these guards help a Day 1 fee agent?

Repeat detection and budget protection can help a Day 1 agent if it uses tools and an iterative loop. Output truncation is particularly useful when tools read external documents or other large sources. Some failures in Day 3 are specifically related to tools that interact with outside data.

---

# 14. Viva Preparation

### What are the six steps of the ReAct loop?

1. Reason
2. Stop if no tool is needed
3. Record the tool request
4. Act
5. Observe
6. Safety exit

### Why use `.get(name)`?

It safely handles a tool name that is not present in the registry.

### Why should tools return error strings?

An error string becomes an observation that the agent can process. Raising an exception can crash the complete agent run.

### Why does `read_webpage()` truncate output?

To prevent excessively large documents from filling the model's context.

### How does repeat detection work?

It records the tool name and arguments. If the same pair is called repeatedly, the agent recognizes that no progress is being made and stops.

### Difference between `max_steps` and `CHAR_BUDGET`

`max_steps` limits the number of agent iterations.

`CHAR_BUDGET` limits the total amount of text sent to the model during one run.

### What are the three main failure modes?

1. Repeating loop → repeat detection
2. Hallucinated/unknown tool → safe registry lookup
3. Context overflow/runaway cost → output truncation and character budget

---

# 15. Final Result

The Day 3 lab successfully demonstrates a ReAct agent built from scratch with a calculator and web-page reader.

The agent is deliberately tested against repeating tool calls, unknown tool requests, and oversized context. Guards are then added to make the agent more reliable.

The final improvements are:

* Repeat detection
* Output truncation
* Character-budget protection
* Safe tool lookup

These changes make the agent stop safely instead of wasting steps, crashing, or processing unnecessarily large tool outputs.
