# Day 2 – Reasoning and Acting

## Comparing Direct Prompting, Chain-of-Thought, and ReAct

This project is part of the **Agentic AI: Foundations and Open-Source Practice – Day 2 Task**.

The project demonstrates how the same type of problem can be handled using three different approaches:

1. Direct Prompting
2. Chain-of-Thought Prompting
3. ReAct Agent

The project also includes a **Self-Consistency experiment** to observe how repeated model responses can vary when the temperature is greater than zero.

---

## 1. Project Objective

The objective of this project is to compare three approaches to solving AI problems:

* **Direct Prompting** answers a question directly using the model's available knowledge.
* **Chain-of-Thought Prompting** encourages careful multi-step reasoning before producing the answer.
* **ReAct** combines reasoning with actions and observations, allowing the agent to use external tools when required.

The project demonstrates the differences in:

* Reasoning depth
* Tool usage
* Reliability on multi-step questions
* Transparency
* Speed and cost
* Consistency across repeated runs

The project also demonstrates self-consistency by running the same reasoning problem multiple times at a non-zero temperature and comparing the results.

---

# 2. Scenario

## College Fee Assistant

The selected scenario is a **College Fee Assistant**.

A student can ask questions about:

* Course fees
* Mathematical calculations
* Course information
* Fee-related reasoning

Some questions can be answered using reasoning alone, while other questions require information from an external tool.

### Available Courses

| Course Code |     Fee |
| ----------- | ------: |
| CS101       | ₹45,000 |
| AI202       | ₹55,000 |
| DS303       | ₹50,000 |

The course fee information is stored inside the project's tool system.

---

# 3. Why This Scenario?

This scenario is suitable because it contains two types of questions.

### Reasoning-only question

Example:

```text
A student scored 80, 70 and 90 in three subjects.
What is the average mark?
```

This question does not require an external information source.

The calculation is:

```text
(80 + 70 + 90) / 3 = 80
```

### Tool-dependent question

Example:

```text
What is the fee for CS101?
```

The exact fee should come from the course-fee tool:

```text
get_course_fee("CS101")
```

The tool returns:

```text
Course: CS101
Fee: ₹45,000
```

This makes it possible to demonstrate the difference between ordinary prompting and an agent that can interact with tools.

---

# 4. System Architecture

```text
                         USER QUESTION
                              |
                              v
                       +--------------+
                       |    main.py   |
                       +--------------+
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
   Direct Prompting          CoT              ReAct Agent
          |                   |                   |
          |                   |                   v
          |                   |             Decide what
          |                   |             information
          |                   |             is required
          |                   |                   |
          |                   |                   v
          |                   |             +-----------+
          |                   |             |   Tools   |
          |                   |             +-----------+
          |                   |                /       \
          |                   |               /         \
          |                   |              v           v
          |                   |       Course Fee      Calculator
          |                   |          Tool            Tool
          |                   |              \           /
          |                   |               \         /
          |                   |                v       v
          |                   |               Observation
          |                   |                   |
          +-------------------+-------------------+
                              |
                              v
                         FINAL ANSWER
```

---

# 5. Project Structure

```text
Day2_task/
│
├── .env
├── .gitignore
├── requirements.txt
│
├── config.py
├── llm_client.py
├── tools.py
│
├── direct_prompting.py
├── chain_of_thought.py
├── react_agent.py
├── self_consistency.py
├── main.py
│
├── README.md
├── analysis.md
│
└── screenshots/
    ├── direct_prompting.png
    ├── chain_of_thought.png
    ├── react_agent.png
    └── self_consistency.png
```

---

# 6. File Description

## `config.py`

Contains the project configuration.

It loads:

* Provider
* Groq API key
* Model name

The API key itself is stored in `.env` and should not be committed to GitHub.

---

## `llm_client.py`

Provides a common function for communicating with the language model.

The other Python files can call:

```python
ask_llm(prompt)
```

instead of creating a new client each time.
