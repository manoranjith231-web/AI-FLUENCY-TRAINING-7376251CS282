# Agentic AI Day 1 – Analysis

## 1. Scenario

The scenario selected for this project is a **College Fee Assistant**.

The assistant answers general college-related questions. It also provides exact course fee information using one external tool.

The course fee data used in the project is:

| Course Code |     Fee |
| ----------- | ------: |
| CS101       | ₹75,000 |
| AI202       | ₹85,000 |
| DS303       | ₹80,000 |

The single tool used in this project is called `get_course_fee`.

For example:

```text
get_course_fee("CS101")
```

returns:

```text
The fee for CS101 is ₹75,000.
```

The scenario was selected because some questions can be answered from the LLM's existing knowledge, while an exact course fee requires access to the external course-fee information.

---

# 2. What is a Large Language Model?

A Large Language Model, or LLM, is a model that can understand text prompts and generate natural-language responses.

In this project, the LLM can answer general questions such as:

```text
What is a college course?
```

It can also answer:

```text
Why is a college course important?
```

These questions do not require the course-fee tool.

However, the LLM does not automatically have access to the current course-fee information used by this project. If it is asked:

```text
What is the exact fee for CS101?
```

the plain LLM cannot verify the value using the project's course-fee data. It should not invent or guess the fee.

Therefore, an LLM is useful for questions that can be answered from its learned knowledge, but an external tool becomes useful when the answer requires specific information or an operation outside the model's available knowledge.

---

# 3. What is an Agent?

An AI agent is a system in which an LLM can decide what action or tool is needed to complete a task.

A plain LLM simply receives a question and generates a response.

A tool-enabled agent can additionally:

1. Understand the question.
2. Decide whether a tool is needed.
3. Request the tool.
4. Receive the tool result.
5. Use the result to produce the final answer.

In this project, the difference can be seen with the course-fee question.

For:

```text
What is a college course?
```

the LLM can answer directly.

For:

```text
What is the exact fee for CS101?
```

the tool-enabled system can recognise that the course-fee tool is needed.

Therefore, the main difference is that a tool-enabled agent can take an action outside the LLM's normal text generation when required.

---

# 4. What is a Tool?

A tool is an external function or capability that an LLM can request when it needs additional information or needs an operation to be performed.

This project uses one tool:

```text
get_course_fee
```

Its purpose is to look up the fee for a course code.

The course fee information is:

```text
CS101 → ₹75,000
AI202 → ₹85,000
DS303 → ₹80,000
```

For example:

```text
get_course_fee("CS101")
```

returns:

```text
The fee for CS101 is ₹75,000.
```

The tool provides information that the plain LLM does not have direct access to.

---

# 5. What is a Tool Call?

A tool call is the request made by the LLM to execute a particular tool with specific input.

For example, when the user asks:

```text
What is the exact fee for CS101?
```

the LLM can request:

```text
Tool: get_course_fee
Course: CS101
```

The Python program then executes the function and obtains the result.

The result is then provided back to the LLM so that it can generate the final response.

---

# 6. What is a Tool Schema?

A tool schema tells the LLM what a tool is called, what it does, and what input it requires.

For this project, the schema describes:

```text
Name:
get_course_fee

Description:
Gets the fee for a college course.

Parameter:
course_code

Parameter type:
string
```

The schema is important because the model needs to understand how the tool should be used.

For example, the model needs to know that the tool expects a course code such as:

```text
CS101
```

rather than an unrelated value.

The schema therefore gives the model enough information to decide whether the tool is relevant and what parameters should be supplied.

---

# 7. Step-by-Step Tool Call Flow

Consider the question:

```text
What is the exact fee for CS101?
```

The complete flow is:

### Step 1 – User asks the question

The user sends:

```text
What is the exact fee for CS101?
```

### Step 2 – LLM receives the question

The LLM analyses the question.

It recognises that the user wants an exact course fee.

### Step 3 – LLM decides that a tool is needed

The course-fee information is available through the `get_course_fee` tool.

The LLM therefore creates a tool call.

### Step 4 – Tool call is made

The request contains:

```text
Tool: get_course_fee
course_code: CS101
```

### Step 5 – Tool runs

The Python function searches the course fee data.

It finds:

```text
CS101 → ₹75,000
```

### Step 6 – Tool result is returned

The tool returns:

```text
The fee for CS101 is ₹75,000.
```

### Step 7 – LLM receives the tool result

The result is provided back to the LLM.

### Step 8 – LLM generates the final answer

The final answer becomes:

```text
The exact fee for CS101 is ₹75,000.
```

The complete flow is:

```text
User
 ↓
Question
 ↓
LLM
 ↓
Tool needed?
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

---

# 8. Why Should a Tool Return Plain Text Even When It Fails?

A tool should return a clear text result instead of stopping the entire program when it cannot find information.

For example, if the user asks for:

```text
CS999
```

and there is no fee information, the tool can return:

```text
No fee information available for CS999.
```

This allows the LLM to receive the result and explain the situation to the user.

Returning a normal text result keeps the interaction going and gives the LLM something meaningful to work with.

The important idea is that a tool result should communicate both successful and unsuccessful outcomes clearly.

---

# 9. Comparison Table

| Basis for Comparison                                        | Plain LLM Prompt                                           | LLM with One Tool                                                                                   |
| ----------------------------------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Source of the answer                                        | The LLM's learned knowledge                                | LLM knowledge plus the tool result                                                                  |
| Can it fetch or compute information outside its own memory? | No                                                         | Yes, through the available tool                                                                     |
| Reliability on factual or numeric questions                 | Can be limited when exact external information is required | Can be improved when the required information is available through the tool                         |
| Transparency                                                | The generated answer does not show an external operation   | The tool call and tool result can be observed                                                       |
| Speed / cost                                                | Usually requires only one LLM response                     | Requires a tool operation and usually another LLM response, so it can involve additional processing |

---

# 10. Question 1 – Observation

## Question

```text
What is a college course?
```

### Plain LLM

The plain LLM can answer this question using its existing knowledge.

Example:

```text
A college course is a subject or unit of study offered by a college to teach knowledge and skills in a specific area.
```

The answer does not require the course-fee tool.

### Tool-Enabled LLM

The tool-enabled version also does not need the tool.

Expected observation:

```text
TOOL USED: NO
```

### Observation

This question can reasonably be answered directly by the LLM.

---

# 11. Question 2 – Observation

## Question

```text
Why is a college course important?
```

### Plain LLM

The plain LLM can answer this question from its existing knowledge.

Example:

```text
A college course helps students gain knowledge and skills needed for their education, career, and personal development.
```

### Tool-Enabled LLM

The tool is not required.

Expected observation:

```text
TOOL USED: NO
```

### Observation

This is another example where the external tool does not provide any necessary information.

The LLM can answer directly.

---

# 12. Question 3 – Observation

## Question

```text
What is the exact fee for CS101?
```

### Plain LLM

The plain LLM does not have access to the project's course-fee tool.

Therefore, it should not guess the exact fee.

Expected response:

```text
I cannot verify the exact fee for CS101 because I do not have access to the college fee database.
```

### Tool-Enabled LLM

The tool-enabled version can call:

```text
get_course_fee
```

with:

```text
course_code = CS101
```

The tool returns:

```text
The fee for CS101 is ₹75,000.
```

The LLM then uses the result to produce:

```text
The exact fee for CS101 is ₹75,000.
```

Expected observation:

```text
TOOL USED: YES
```

### Observation

This question demonstrates the main purpose of the tool.

The exact fee cannot be verified by the plain LLM, while the tool-enabled version can obtain the required value from the course-fee data.

---

# 13. Overall Observation

The three questions demonstrate two different types of situations.

The first two questions are general knowledge questions. The LLM can answer them without external help.

The third question asks for an exact numeric value from the scenario's course-fee data. The tool-enabled version can retrieve that value using the external tool.

The experiment therefore shows that a tool is not necessary for every question. It becomes useful when the question requires specific information that is not available directly to the model.

---

# 14. Suitability of the Plain LLM

A plain LLM is suitable when:

* The question is general.
* The answer can reasonably come from the model's learned knowledge.
* No current or private external information is required.
* No external calculation or operation is necessary.

In this project, the questions about what a college course is and why a course is important are suitable for a plain LLM.

---

# 15. When the External Tool Becomes Necessary

The external tool becomes necessary when the answer depends on specific information that the LLM cannot reliably retrieve from its own knowledge.

In this project, the exact fee of CS101 is stored in the course-fee tool.

Therefore, the tool-enabled version is required to retrieve:

```text
CS101 → ₹75,000
```

The tool provides the information and the LLM uses that result to form the final answer.

---

# 16. General Conclusion

This experiment demonstrates the basic difference between a plain LLM and an LLM with access to one tool.

A plain LLM can answer many general questions directly from its learned knowledge. However, it cannot automatically access the specific course-fee data used in this project.

Adding one tool gives the LLM a way to obtain information outside its normal text-generation capability.

The important workflow is:

```text
Question
   ↓
LLM
   ↓
Decide whether a tool is needed
   ↓
Tool Call
   ↓
Tool Result
   ↓
LLM
   ↓
Final Answer
```

The experiment also shows that tool use should be based on the requirement of the question. General questions can be answered directly, while questions requiring specific external information may require a tool.

Therefore, a plain LLM prompt is sufficient when the task can be answered reliably from the model's existing knowledge. A tool should be provided when the task requires external information, an operation, a lookup, or another capability that the model cannot reliably perform by generating text alone.
