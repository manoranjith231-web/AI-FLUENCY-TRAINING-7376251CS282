# Agentic AI – College Fee Assistant

## 1. Project Title

**From Prompt to Action: Understanding LLMs, Tools, and Agents**

### Scenario: College Fee Assistant

This project demonstrates the difference between a plain Large Language Model (LLM) and an LLM that has access to one external tool.

The selected scenario is a **College Fee Assistant**.

The assistant can answer general college-related questions directly using the LLM. When a user asks for an exact course fee, the tool-enabled version can use a course-fee lookup tool to obtain the required information.

---

## 2. Project Objective

The objective of this project is to understand:

* What an LLM is
* What an AI agent is
* What a tool is
* What a tool call is
* What a tool schema is
* How an LLM decides whether a tool is required
* How the tool result is returned to the LLM
* The difference between a plain LLM and a tool-enabled LLM

The project uses only **one external tool**, as required by the assignment.

---

## 3. Scenario

The College Fee Assistant contains the following course fee information:

| Course Code | Course Fee |
| ----------- | ---------: |
| CS101       |    ₹75,000 |
| AI202       |    ₹85,000 |
| DS303       |    ₹80,000 |

This information is stored in the course-fee tool.

For example, when the user asks:

```text
What is the exact fee for CS101?
```

the tool can return:

```text
The fee for CS101 is ₹75,000.
```

The LLM can then use this result to provide the final answer.

---

## 4. Project Structure

```text
day3_task/
│
├── .env
├── .gitignore
├── requirements.txt
│
├── tool.py
├── no_tool.py
├── with_tool.py
│
├── README.md
├── analysis.md
│
└── screenshots/
    ├── no_tool.png
    └── with_tool.png
```

### File Description

| File               | Purpose                                                   |
| ------------------ | --------------------------------------------------------- |
| `tool.py`          | Contains the single course-fee lookup tool                |
| `no_tool.py`       | Runs the LLM without tool access                          |
| `with_tool.py`     | Runs the LLM with the course-fee tool                     |
| `requirements.txt` | Contains required Python packages                         |
| `.env`             | Stores the Groq API key                                   |
| `.gitignore`       | Prevents sensitive/unnecessary files from being committed |
| `README.md`        | Project documentation                                     |
| `analysis.md`      | Full assignment analysis                                  |
| `screenshots/`     | Output screenshots of both runs                           |

---

## 5. Technologies Used

* Python
* Groq API
* Groq Python SDK
* Python-dotenv
* `openai/gpt-oss-120b`

---

## 6. Requirements

Install the required packages using:

```powershell
pip install -r requirements.txt
```

The `requirements.txt` file contains:

```text
groq
python-dotenv
```

---

## 7. Environment Setup

Create a `.env` file in the project directory:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Replace the value with the actual Groq API key.

The API key should never be uploaded to GitHub.

The `.gitignore` file contains:

```text
.env
.venv/
__pycache__/
*.pyc
```

---

## 8. How to Run

### Run the Plain LLM

The plain LLM has no access to the course-fee tool.

Run:

```powershell
python no_tool.py
```

It can answer general questions but cannot verify the exact course fee from the external course-fee data.

---

### Run the Tool-Enabled LLM

The tool-enabled version has access to one tool:

```text
get_course_fee
```

Run:

```powershell
python with_tool.py
```

When the question requires the exact course fee, the LLM can request the tool.

---

## 9. Questions Used

The project tests three questions:

### Question 1

```text
What is a college course?
```

This does not require the external tool.

### Question 2

```text
Why is a college course important?
```

This also does not require the external tool.

### Question 3

```text
What is the exact fee for CS101?
```

This requires the course-fee tool.

---

## 10. Tool Flow

The tool-enabled program follows this process:

```text
User Question
      ↓
LLM
      ↓
Does the question need the tool?
      ↓
     YES
      ↓
Tool Call
      ↓
get_course_fee("CS101")
      ↓
Tool Result
      ↓
LLM
      ↓
Final Answer
```

For a general question:

```text
User Question
      ↓
LLM
      ↓
Final Answer
```

No tool call is necessary.

---

## 11. Expected Tool Example

For:

```text
What is the exact fee for CS101?
```

the tool-enabled program should show something similar to:

```text
[TOOL CALL]
Tool: get_course_fee
Course: CS101

[TOOL RESULT]
The fee for CS101 is ₹75,000.

ANSWER
The exact fee for CS101 is ₹75,000.

TOOL USED: YES
```

---

## 12. Plain LLM vs Tool-Enabled LLM

| Feature                      | Plain LLM | LLM with One Tool |
| ---------------------------- | --------- | ----------------- |
| Uses LLM                     | Yes       | Yes               |
| External tool available      | No        | Yes               |
| General questions            | Yes       | Yes               |
| Course fee lookup            | No        | Yes               |
| Tool call                    | No        | Yes               |
| Can use external course data | No        | Yes               |

---

## 13. Screenshots

The `screenshots` folder contains the outputs of both runs.

Recommended screenshots:

```text
screenshots/
├── no_tool.png
└── with_tool.png
```

The `with_tool.png` screenshot should clearly show:

1. The question
2. The tool call
3. The tool result
4. The final answer

---

## 14. Learning Outcome

This project demonstrates that an LLM can answer many general questions using its existing knowledge.

However, when a question requires specific information that is not available to the LLM, an external tool can provide the required information.

The project therefore demonstrates the basic idea of:

```text
LLM + Tool + Action
```

and shows how tool access can improve the reliability of answers for specific factual or numeric questions.
