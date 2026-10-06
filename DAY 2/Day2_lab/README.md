# Agentic AI – Day 2 Lab

## Reasoning and Acting: ReAct, Direct Prompting, Chain-of-Thought and Self-Consistency

This project is part of **Agentic AI: Foundations and Open-Source Practice – Day 2**.

The objective of this lab is to understand how an AI system solves problems using different prompting and agentic approaches:

* Direct Prompting
* Chain-of-Thought (CoT)
* ReAct (Reasoning + Acting)
* Self-Consistency

The lab compares these approaches and studies when reasoning alone is sufficient and when external tools are required.

---

## 1. Aim

The aim of this project is to:

* Understand the Thought → Action → Observation cycle of a ReAct agent.
* Compare direct prompting with Chain-of-Thought prompting.
* Understand how external tools improve an AI agent's ability to answer questions requiring external information.
* Experiment with self-consistency using multiple reasoning attempts.
* Compare the accuracy, steps, and behavior of different approaches.

---

## 2. Scenario

### College Fee Assistant

A college fee assistant is used as the scenario for the agent.

The assistant works with the following course fee information:

| Course |     Fee |
| ------ | ------: |
| CS101  | ₹12,000 |
| AI202  | ₹18,000 |
| DS303  | ₹15,000 |

The agent can use two main tools:

```text
get_course_fee(course_code)
calculator(expression)
```

The `get_course_fee()` tool retrieves the actual course fee, while the `calculator()` tool performs arithmetic operations.

---

## 3. Day 2 Problem Statement

The main ReAct question is:

> Which is cheaper: CS101 and AI202 with a 10% scholarship, or all three courses with a 25% scholarship? And by how much?

### Calculation

#### Option 1

CS101 + AI202:

```text
₹12,000 + ₹18,000 = ₹30,000
```

After 10% scholarship:

```text
₹30,000 × 0.9 = ₹27,000
```

#### Option 2

All three courses:

```text
₹12,000 + ₹18,000 + ₹15,000 = ₹45,000
```

After 25% scholarship:

```text
₹45,000 × 0.75 = ₹33,750
```

Difference:

```text
₹33,750 - ₹27,000 = ₹6,750
```

Therefore, the first option costs **₹6,750 less**.

---

## 4. Reasoning Questions

The project also uses reasoning-only questions that do not require external tools.

### Question 1 – Instalment Calculation

A student takes three courses costing ₹12,000, ₹18,000 and ₹15,000. She receives a 15% scholarship and pays the remaining amount in 4 equal instalments.

Expected answer:

```text
₹9,562.50 per instalment
```

### Question 2 – Lab Sittings

A lab has 18 computers. Each computer is shared by 2 students in the morning and 3 students in the afternoon.

Calculation:

```text
(18 × 2) + (18 × 3) = 90
```

Expected answer:

```text
90 student sittings
```

### Question 3 – Logical Ordering

Ravi is taller than Kumar. Kumar is taller than Arun. Priya is shorter than Arun.

Expected answer:

```text
Tallest: Ravi
Shortest: Priya
```

---

## 5. Approaches Used

### 5.1 Direct Prompting

Direct prompting asks the model to provide an answer without explicitly requesting step-by-step reasoning.

Example:

```text
Give only the final answer.
```

### Advantages

* Simple
* Fast
* Uses fewer output tokens
* Easy to implement

### Limitations

* May make mistakes on multi-step calculations.
* Does not provide a visible reasoning process.
* Cannot access external information without tools.

---

## 5.2 Chain-of-Thought Prompting

Chain-of-Thought prompting asks the model to solve a problem step by step.

Example:

```text
Solve the problem step by step.
Number each step and show the calculation.
```

The model can break a problem into smaller steps before producing the final answer.

### Advantages

* Useful for multi-step reasoning.
* Makes calculations easier to follow.
* Can improve accuracy on reasoning problems.

### Limitations

* Requires more output tokens.
* Takes longer than a direct answer.
* Cannot retrieve external information by itself.
* If required information is missing, the model may produce an incorrect or invented value.

---

## 5.3 ReAct

ReAct combines reasoning with actions.

The general cycle is:

```text
Thought
   ↓
Action
   ↓
Observation
   ↓
Thought
   ↓
Action
   ↓
Observation
   ↓
Final Answer
```

For the college fee problem, the agent can:

1. Retrieve CS101 fee.
2. Retrieve AI202 fee.
3. Retrieve DS303 fee.
4. Calculate the first option.
5. Calculate the second option.
6. Calculate the difference.
7. Generate the final answer.

### Example Tool Calls

```text
get_course_fee("CS101")
get_course_fee("AI202")
get_course_fee("DS303")
calculator("(12000 + 18000) * 0.9")
calculator("(12000 + 18000 + 15000) * 0.75")
calculator("33750 - 27000")
```

### Advantages

* Can use external tools.
* Can retrieve information that is not stored in the model's knowledge.
* Suitable for multi-step tasks.
* Can verify calculations using tools.

### Limitations

* More tool calls increase execution time.
* More calls can increase API usage/cost.
* The agent may select an incorrect tool or argument.
* Small models may sometimes stop early or produce incorrect actions.

---

## 5.4 Self-Consistency

Self-consistency runs the same reasoning problem multiple times with a non-zero temperature.

In this project:

```text
RUNS = 5
TEMPERATURE = 0.8
```

The final answers from the five runs are collected and the most frequent answer is selected as the majority answer.

Example:

```text
Run 1 → ₹9,562.50
Run 2 → ₹9,562.50
Run 3 → ₹11,250
Run 4 → ₹9,562.50
Run 5 → ₹9,562.50

Majority → ₹9,562.50
```

The actual values obtained during the experiment should be recorded in the final analysis.

### Why temperature is non-zero

A temperature of `0` makes responses highly similar.

Self-consistency requires different reasoning attempts, so a higher temperature is used.

---

## 6. Comparison

| Feature              | Direct Prompting | Chain-of-Thought | ReAct                        |
| -------------------- | ---------------- | ---------------- | ---------------------------- |
| Reasoning            | Minimal          | Step-by-step     | Reasoning + actions          |
| External tools       | No               | No               | Yes                          |
| Multi-step problems  | Moderate         | Better           | Strong when tools are needed |
| External information | Cannot retrieve  | Cannot retrieve  | Can retrieve using tools     |
| Speed                | Fast             | Slower           | Depends on tool calls        |
| Output length        | Short            | Longer           | Variable                     |
| Main purpose         | Direct answers   | Reasoning        | Reasoning + tool use         |

---

## 7. Project Structure

```text
Day2_task/
│
├── .env
├── .gitignore
├── config.py
├── tools.py
├── llm_client.py
├── direct_prompting.py
├── chain_of_thought.py
├── react_agent.py
├── self_consistency.py
├── main.py
├── requirements.txt
├── README.md
├── analysis.md
│
└── screenshots/
    ├── direct_q1.png
    ├── direct_q2.png
    ├── cot_q1.png
    ├── cot_q2.png
    ├── react_q1.png
    ├── react_q2.png
    ├── self_consistency_q1.png
    └── self_consistency_q2.png
```

> `.env` contains the API key and must not be uploaded to GitHub.

---

## 8. Technologies Used

* Python
* Groq API
* Groq Python SDK
* `python-dotenv`
* Large Language Model
* ReAct agent pattern
* Chain-of-Thought prompting
* Self-consistency

---

## 9. Installation

Create and activate the virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

Install the required packages:

```powershell
pip install groq python-dotenv
```

Or:

```powershell
pip install -r requirements.txt
```

---

## 10. Environment Configuration

Create a `.env` file:

```text
PROVIDER=groq
GROQ_API_KEY=YOUR_API_KEY
MODEL=openai/gpt-oss-20b
```

Do not upload the `.env` file to GitHub.

---

## 11. Running the Programs

### Direct Prompting

```powershell
python direct_prompting.py
```

### Chain-of-Thought

```powershell
python chain_of_thought.py
```

### ReAct Agent

```powershell
python react_agent.py
```

### Self-Consistency

```powershell
python self_consistency.py
```

### Main Menu

All approaches can also be accessed through:

```powershell
python main.py
```

---

## 12. ReAct Execution Flow

For a question requiring external information, the ReAct agent follows this pattern:

```text
User Question
      ↓
   Thought
      ↓
 Select Tool
      ↓
    Action
      ↓
   Tool Call
      ↓
 Observation
      ↓
   Further Thought
      ↓
 Additional Tool Call
      ↓
   Observation
      ↓
 Final Answer
```

This demonstrates how an AI agent differs from a normal chatbot.

---

## 13. Self-Consistency Experiment

The self-consistency experiment uses the same reasoning question multiple times.

The process is:

```text
Question
   ↓
CoT Run 1
CoT Run 2
CoT Run 3
CoT Run 4
CoT Run 5
   ↓
Collect Final Answers
   ↓
Majority Voting
   ↓
Final Majority Answer
```

The majority answer is then compared with the correct answer and with the result obtained using temperature `0`.

---

## 14. Screenshots

The `screenshots` folder contains the outputs of the experiments.

The screenshots demonstrate:

1. Direct Prompting
2. Chain-of-Thought
3. ReAct tool usage
4. Self-Consistency

For the ReAct experiment, the output should demonstrate the agent's tool interaction and observations.

---

## 15. Learning Outcomes

After completing this project, the following concepts were understood:

* Difference between normal prompting and reasoning prompts.
* Chain-of-Thought for multi-step reasoning.
* ReAct for combining reasoning and external actions.
* Tool calling in AI agents.
* Thought → Action → Observation cycles.
* Self-consistency and majority voting.
* Importance of external tools when information is unavailable to the model.
* Trade-offs between accuracy, speed, and API usage.

---

## 16. Conclusion

This project demonstrates that different AI approaches are suitable for different types of problems.

Direct prompting is useful for simple questions. Chain-of-Thought can improve performance on problems that require multiple reasoning steps. However, reasoning alone cannot retrieve information that is not available to the model.

ReAct addresses this limitation by allowing the agent to interact with external tools, observe their results, and continue reasoning before producing the final answer.

Self-consistency provides another way to improve reliability by generating multiple reasoning attempts and selecting the most common final answer.

Overall, the experiment demonstrates the difference between a model that only generates an answer and an agent that can reason, act, observe, and use tools.
