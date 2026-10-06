# Comparing a Plain Chatbot, Rule-Based Workflow, and AI Agent

## 1. Introduction

This project demonstrates the difference between a plain chatbot, a
rule-based workflow, and an AI agent by applying all three approaches
to the same private-data scenario.

The selected scenario is a Private Student Academic Assistant. The
system contains student information, subject marks, attendance
percentages, and assignment status.

The same types of questions are given to all three systems. The
purpose is to observe how their architectures affect private-data
access, decision-making, tool usage, flexibility, multi-step task
handling, automation, and reliability.

The three architectures can be summarized as follows:

- Plain chatbot: LLM-based response generation without direct private
  data access or tools in this implementation.
- Rule-based workflow: predefined rules and conditions that directly
  operate on private data.
- AI agent: LLM/agent decision-making combined with tools and an
  iterative loop.

The central concept demonstrated by this project is:

**Agent = LLM + Tools + Loop**

---

# 2. Scenario

The selected scenario is a private student academic assistant.

The system contains the following types of information:

- Student name
- Department
- Year
- Semester
- Subject marks
- Attendance percentage
- Assignment completion status

The demonstration uses synthetic data stored in
`data/student_data.json`.

Example questions include:

1. What is my DBMS mark?
2. Which subjects have pending assignments?
3. Which subjects have attendance below 80%?
4. Show my student details.
5. Show information about Python.

The same scenario is implemented using three different architectures.

---

# 3. Private Data

The private data is stored locally in the following file:

`data/student_data.json`

The data contains student and academic information.

The file is not accessed by the plain chatbot.

The rule-based workflow directly reads the JSON file.

The AI agent accesses the data through controlled Python tools such as
`get_subject_info()`, `get_pending_assignments()`, and
`get_low_attendance()`.

This difference is important because it demonstrates how an AI agent
can interact with private data through tools rather than simply
generating an answer from the language model.

The data used in this project is synthetic demonstration data and is
not intended to represent an actual academic database.

---

# 4. Plain Chatbot

## 4.1 How it works

The plain chatbot is the simplest architecture in this project.

Its basic structure is:

User -> Chatbot/LLM -> Response

The chatbot receives the user's question and generates a response.
There are no external tools and there is no direct connection to the
private student data file.

The implementation demonstrates the conceptual behavior of an LLM
chatbot rather than connecting the program to an external language
model API.

---

## 4.2 Data access

The plain chatbot does not access `student_data.json`.

Therefore, if the user asks:

"What is my DBMS mark?"

the chatbot cannot retrieve the actual DBMS mark from the private
file.

It instead explains that it does not have access to the private
student records.

---

## 4.3 Tools

The plain chatbot does not use tools.

It does not have functions for reading student records, checking
attendance, or finding assignments.

---

## 4.4 Request handling

The chatbot receives the user's question and generates a general
response.

For example:

User:

"What is my DBMS mark?"

The chatbot responds that it cannot access the private student
records.

This demonstrates that response generation alone is different from
performing an action on private data.

---

## 4.5 Limitations

The main limitation is the lack of private-data access.

It also cannot perform database-style operations such as searching
subjects or checking attendance unless that capability is explicitly
provided to it.

The chatbot is therefore useful for conversation and explanation, but
the implementation does not provide the tools required to retrieve
the student's private information.

---

# 5. Rule-Based Workflow

## 5.1 How it works

The rule-based workflow follows predefined conditions.

Its architecture is:

User -> Predefined Rules -> Private Data -> Response

There is no LLM involved.

The program checks the user's question against predefined conditions.

For example, the program contains rules for:

- DBMS marks
- Pending assignments
- Attendance
- Attendance below 80%
- Student information
- All subjects

---

## 5.2 Data access

The rule-based workflow directly reads the
`student_data.json` file.

Therefore, it can retrieve the actual private information.

For example, when the user asks about DBMS marks, the workflow checks
the predefined DBMS rule and retrieves the marks from the JSON data.

---

## 5.3 Rules

The workflow uses conditions such as:

- If the question contains "DBMS" and "mark", retrieve DBMS marks.
- If the question contains "pending" and "assignment", find pending
  assignments.
- If the question contains "attendance", display attendance.
- If the question asks about attendance below 80%, filter the subjects
  using the predefined threshold.

These rules are explicitly programmed.

---

## 5.4 Request handling

Suppose the user asks:

"Which subjects have pending assignments?"

The workflow checks the predefined condition for pending assignments.

It then examines every subject in the JSON file and checks whether the
assignment status is "Pending".

The resulting subjects are displayed.

For the demonstration data, the result is:

- DBMS
- Operating Systems

---

## 5.5 Limitations

The main limitation is that the workflow depends on predefined
conditions.

If the user asks a question that has not been anticipated by the
program, the workflow may not know how to process it.

Adding new types of requests requires additional rules.

The workflow is therefore predictable for the cases it was explicitly
programmed to handle, but it is less flexible when the request changes.

---

# 6. AI Agent

## 6.1 How it works

The AI agent combines decision-making, tools, observations, and a loop.

Its conceptual architecture is:

User
|
v
LLM / Agent Decision
|
v
Tool Selection
|
v
Tool Execution
|
v
Observation
|
v
Agent Decision
|
v
Final Answer

The key concept is:

**Agent = LLM + Tools + Loop**

The implementation in this project demonstrates the agent architecture
using an agent decision layer and multiple private-data tools.

---

## 6.2 Tools

The agent has the following tools:

### `get_student_info()`

Returns basic student information.

### `get_subject_info(subject)`

Returns the marks, attendance, and assignment status for a subject.

### `get_pending_assignments()`

Finds subjects whose assignments are pending.

### `get_low_attendance(threshold)`

Finds subjects whose attendance is below a specified threshold.

### `get_all_subjects()`

Returns all subject information.

These tools provide controlled access to the private student data.

---

## 6.3 Tool selection

The agent examines the user's request and selects an appropriate tool.

For example:

User:

"Which subjects have pending assignments?"

The agent identifies that the pending-assignment tool is relevant.

It selects:

`get_pending_assignments()`

The tool accesses the private data and returns:

- DBMS
- Operating Systems

The agent then observes this result and produces the final response.

---

## 6.4 Agent loop

The agent follows an iterative process:

1. Receive the user's request.
2. Analyze what type of task is required.
3. Select an appropriate tool.
4. Execute the tool.
5. Observe the result.
6. Process the observation.
7. Produce the final answer.

The important difference from a fixed workflow is that an agent
architecture is designed around deciding what action should be taken
rather than simply following one fixed sequence for every request.

The demonstration shows the tool selection, tool call, observation, and
final answer explicitly in the terminal output.

---

## 6.5 Private-data access

The agent does not need to expose the entire private JSON file to the
user.

Instead, access is provided through tools.

For example:

`get_subject_info("DBMS")`

returns only the relevant information about DBMS.

This provides a controlled mechanism for connecting the agent to
private information.

---

## 6.6 Limitations

The agent depends on the quality of its decision-making and the
correctness of the tools.

An incorrect tool selection can produce an incorrect or incomplete
answer.

The tools themselves must also be implemented correctly.

If the private data is incorrect, the agent cannot produce correct
information from that data.

Therefore, an agent does not automatically guarantee correctness just
because it can use tools.

---

# 7. Comparison

| Basis for comparison | Plain chatbot | Rule-based workflow | AI agent |
|---|---|---|---|
| Flexibility | Can generate conversational responses but has no private-data capability in this implementation | Limited to predefined rules | Can select tools based on the task |
| Decision-making | Generates a response but does not perform private-data operations | Uses fixed conditions | Uses an agent decision process to select actions/tools |
| Tool usage | No tools | Uses programmed functions as part of fixed rules | Uses tools selected according to the task |
| Private-data access | No direct access | Directly reads the JSON data | Accesses private data through tools |
| Multi-step task handling | Limited in this implementation | Must be explicitly programmed | Can use a loop to perform multiple actions |
| Automation | Mainly response generation | Automates predefined processes | Can automate tasks involving decisions and tools |
| Reliability | Depends on generated responses and available information | Predictable for explicitly programmed cases | Depends on the LLM/decision process, tools, data, and validation |

---

# 8. Comparison Analysis

## Flexibility

The plain chatbot can respond flexibly to natural-language questions,
but in this implementation it cannot retrieve private academic
information.

The rule-based workflow is less flexible because its supported
questions are defined by explicit conditions.

The AI-agent architecture provides a mechanism for interpreting a
task, selecting tools, and continuing the process based on tool
results.

---

## Decision-making

The plain chatbot mainly generates a response.

The rule-based workflow makes decisions through predefined `if`
conditions.

The AI agent introduces an agent decision layer that determines which
tool should be used for the current task.

---

## Tool usage

The plain chatbot does not use tools.

The rule-based workflow uses Python functions, but they are connected
to predetermined conditions.

The AI agent treats functions as tools that can be selected according
to the user's task.

---

## Private-data access

The plain chatbot in this project has no access to the private JSON
file.

The rule-based workflow directly reads the file.

The AI agent accesses the data through controlled tools.

This demonstrates three different levels of interaction with private
information.

---

## Multi-step task handling

The plain chatbot implementation does not perform multi-step
private-data operations.

The rule-based workflow can perform multiple operations if those
operations have been explicitly programmed.

An agent architecture can repeatedly decide, use a tool, observe the
result, and continue when more work is needed.

---

## Automation

The chatbot automates response generation.

The rule-based workflow automates predictable academic-data queries.

The agent architecture can automate tasks where the system needs to
select tools and process their results.

---

## Reliability

Each approach has different reliability considerations.

A rule-based workflow can be predictable for the cases covered by its
rules.

A chatbot's response depends on the information available to it and
the generated response.

An agent depends on several components: the decision-making model,
tools, private data, and validation.

Therefore, tool access alone does not guarantee correct results.

---

# 9. Suitability Analysis

The appropriate architecture depends on the requirements of the task.

The plain chatbot is suitable when the main requirement is
conversation, explanation, brainstorming, or response generation and
private-data operations are not required.

The rule-based workflow is suitable when the process is predictable
and the possible inputs and actions can be clearly defined in advance.
For example, checking whether an assignment is pending can be
implemented using explicit conditions.

The AI-agent architecture is suitable when the task requires flexible
decision-making and interaction with one or more tools. In this
scenario, the agent can choose between tools for subject information,
pending assignments, attendance, and student information.

The student academic assistant therefore provides a useful example of
why different architectures exist. A simple request may not require
an agent, while a request requiring private-data access and multiple
actions can benefit from a tool-using agent architecture.

---

# 10. Conclusion

A plain chatbot, a rule-based workflow, and an AI agent represent
different approaches to solving software problems.

A plain chatbot mainly uses an LLM to understand input and generate
responses. It is useful for conversation and information-oriented
interaction.

A rule-based workflow uses predefined steps, conditions, and actions.
It is useful when the process is predictable and the possible
situations can be defined in advance.

An AI agent combines an LLM or decision-making model with tools and a
loop. It can decide which tool is appropriate, execute the tool,
observe the result, and continue until the task is completed.

The key concept demonstrated by this project is:

**Agent = LLM + Tools + Loop**

The choice between these architectures should depend on the problem.
Chatbots are appropriate for response generation and conversation,
rule-based workflows are appropriate for predictable processes, and
AI-agent architectures are appropriate for tasks requiring flexible
decision-making and interaction with tools.