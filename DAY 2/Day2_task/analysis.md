# Day 2 Analysis – Reasoning and Acting

## Comparing Direct Prompting, Chain-of-Thought, and ReAct

## 1. Introduction

This project compares three approaches for solving AI problems: Direct Prompting, Chain-of-Thought Prompting, and a ReAct Agent.

The selected scenario is a **College Fee Assistant**. The scenario contains both reasoning-based questions and questions that require external information. This makes it possible to demonstrate the differences between a normal language-model response, a reasoning-oriented prompt, and an agent that can use tools.

The three approaches are compared based on reasoning depth, tool usage, reliability on multi-step questions, transparency, speed and cost, and consistency across repeated runs.

A self-consistency experiment is also performed to observe the effect of non-zero temperature on repeated answers.

---

# 2. Scenario – College Fee Assistant

The scenario used in this project is a College Fee Assistant.

The assistant can answer questions related to course fees and perform calculations.

The available course information is:

| Course Code |     Fee |
| ----------- | ------: |
| CS101       | ₹45,000 |
| AI202       | ₹55,000 |
| DS303       | ₹50,000 |

The course fees are stored in the project's tool system.

For example:

```text
get_course_fee("CS101")
```

returns:

```text
Course Code: CS101
Fee: ₹45,000
```

The scenario contains two important types of questions.

### Reasoning question

```text
A student scored 80, 70 and 90 in three subjects.
What is the average mark?
```

The calculation is:

```text
(80 + 70 + 90) / 3 = 80
```

This question can be solved using reasoning and arithmetic.

### External-information question

```text
What is the fee for CS101?
```

This question requires the exact fee stored in the external tool.

Therefore, the scenario allows the three approaches to be compared meaningfully.

---

# 3. Direct Prompting

## 3.1 How Direct Prompting Works

Direct prompting sends the user's question directly to the language model.

The model receives the question and generates an answer using the information available to it.

The basic flow is:

```text
User Question
      |
      v
Language Model
      |
      v
Final Answer
```

There is no separate tool call in the Direct Prompting implementation.

The model is instructed to answer directly without using external tools.

---

## 3.2 What Direct Prompting Can Answer

Direct prompting can answer questions that depend on:

* General knowledge available to the model
* Simple calculations
* Straightforward explanations
* Basic reasoning

For example:

```text
What is 25 + 35?
```

can be answered directly.

It can also solve:

```text
A student scored 80, 70 and 90.
What is the average?
```

because the required information is already included in the question.

---

## 3.3 What Direct Prompting Cannot Reliably Answer

Direct prompting does not have access to the project's course-fee tool.

Therefore, when asked:

```text
What is the exact fee for CS101?
```

the model cannot retrieve the fee using `get_course_fee()`.

This is an important limitation.

If the exact information is not available to the model, direct prompting cannot independently retrieve it from the project's external data source.

---

## 3.4 Tool Usage

Direct Prompting does not use tools.

The flow is:

```text
Question
   ↓
Model
   ↓
Answer
```

There is no:

```text
Action
Observation
```

cycle.

---

## 3.5 Limitation in This Scenario

The main limitation is the lack of external information access.

For reasoning-only questions, Direct Prompting can be sufficient.

For exact course-fee questions, it cannot use the project's fee database.

---

# 4. Chain-of-Thought Prompting

## 4.1 How Chain-of-Thought Works

Chain-of-Thought prompting asks the model to carefully reason through a problem before producing its final response.

The conceptual flow is:

```text
User Question
      |
      v
Careful Internal Reasoning
      |
      v
Final Answer
```

In this project, the model is instructed to perform reasoning internally and provide a concise explanation rather than exposing private chain-of-thought.

---

## 4.2 Reasoning Example

Question:

```text
A student scored 80, 70 and 90 in three subjects.
What is the average?
```

The calculation is:

```text
80 + 70 + 90 = 240

240 / 3 = 80
```

Therefore:

```text
Average = 80
```

The reasoning approach helps the model handle the multiple steps in the calculation.

---

## 4.3 What Chain-of-Thought Can Answer

Chain-of-Thought prompting can help with:

* Multi-step arithmetic
* Logical problems
* Problems requiring several intermediate steps
* Structured reasoning
* Problems where all necessary information is provided in the prompt

---

## 4.4 What Chain-of-Thought Cannot Do

Reasoning does not automatically provide access to external information.

For example:

```text
What is the exact fee for CS101?
```

If the fee information is not available to the model, reasoning alone cannot retrieve it from the project's course-fee tool.

This demonstrates an important distinction:

```text
Better reasoning
        ≠
External information access
```

---

## 4.5 Tool Usage

The Chain-of-Thought implementation does not use external tools.

Therefore:

```text
Question
   ↓
Internal reasoning
   ↓
Answer
```

There is no tool call.

---

## 4.6 Limitation in This Scenario

The main limitation is that the approach can reason about information provided to it, but it cannot call the course-fee tool to retrieve an exact fee.

Therefore, it is useful for the average-mark question but not sufficient by itself for the external-information question.

---

# 5. ReAct Agent

## 5.1 What ReAct Means

ReAct combines reasoning and acting.

Instead of only generating an answer, the agent can determine that it needs additional information, perform an action using a tool, observe the result, and then produce the final answer.

The conceptual cycle is:

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

The actual number of cycles depends on the problem.

---

# 5.2 ReAct in This Project

The ReAct agent has access to two tools:

### Tool 1 – Course Fee Tool

```text
get_course_fee(course_code)
```

It retrieves the fee of a course.

### Tool 2 – Calculator

```text
calculator(expression)
```

It performs arithmetic.

---

# 5.3 Example ReAct Execution

User question:

```text
What is the fee for CS101?
```

The agent first determines that it needs exact course-fee information.

### Thought

```text
The exact fee of CS101 is required, so I need the course fee tool.
```

### Action

```text
get_course_fee("CS101")
```

### Observation

```text
Course Code: CS101
Fee: ₹45,000
```

### Final Answer

```text
The fee for CS101 is ₹45,000.
```

The important difference is that the final answer is based on the tool observation.

---

# 5.4 Why ReAct Is Different

Direct Prompting:

```text
Question → Answer
```

Chain-of-Thought:

```text
Question → Reasoning → Answer
```

ReAct:

```text
Question
   ↓
Reason
   ↓
Action
   ↓
Observation
   ↓
Reason
   ↓
Answer
```

Therefore, ReAct can combine reasoning with external information.

---

# 5.5 ReAct Tool Decision

The agent determines whether a tool is required.

For example:

```text
What is 25 + 35?
```

may not require an external course-fee lookup.

However:

```text
What is the fee for CS101?
```

requires:

```text
get_course_fee
```

The agent uses the result before generating the final answer.

---

# 5.6 Limitation of ReAct

ReAct introduces additional complexity.

The agent must:

1. Select the correct tool.
2. Provide the correct argument.
3. Interpret the tool result.
4. Use the result correctly.
5. Produce the final response.

Therefore, although ReAct provides greater capability, it also involves additional steps compared with direct prompting.

---

# 6. Comparison Table

| Basis                               | Direct Prompting                                   | Chain-of-Thought                                                                    | ReAct Agent                                                              |
| ----------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Reasoning depth                     | Basic/direct                                       | Better for multi-step reasoning                                                     | Reasoning combined with actions                                          |
| Tool usage                          | No tools                                           | No tools                                                                            | Uses external tools                                                      |
| Reliability on multi-step questions | Suitable for simple problems                       | Better for multi-step reasoning                                                     | Useful when reasoning and external information are both required         |
| Transparency                        | Final answer is visible; internal reasoning is not | Final answer and concise explanation can be shown; private reasoning is not exposed | Tool selection, action and observation can be shown                      |
| Speed / cost                        | Generally lowest overhead                          | More reasoning may require more computation                                         | Higher overhead because of tool calls and additional steps               |
| Consistency across repeated runs    | Can vary depending on temperature                  | Can vary depending on temperature                                                   | Can vary because both model decisions and tool interactions are involved |

---

# 7. Reasoning Depth Comparison

Direct Prompting performs the smallest amount of explicit processing from the application's perspective.

It is appropriate when the question is simple and the required information is already available to the model.

Chain-of-Thought provides a stronger reasoning approach for problems containing multiple steps.

ReAct extends this further by allowing the agent to interact with external tools.

The progression can therefore be represented as:

```text
Direct Prompting
       ↓
Reasoning
       ↓
Chain-of-Thought
       ↓
Reasoning + Tools
       ↓
ReAct
```

This does not mean that ReAct is automatically necessary for every question. The appropriate approach depends on the problem.

---

# 8. Tool Usage Comparison

Direct Prompting:

```text
No tool
```

Chain-of-Thought:

```text
No tool
```

ReAct:

```text
Tool selection
     ↓
Tool execution
     ↓
Observation
     ↓
Final response
```

In this scenario, ReAct is the only approach that can directly retrieve the course fee from the project's tool.

---

# 9. Reliability on Multi-Step Questions

For a simple calculation such as:

```text
25 + 35
```

Direct Prompting is sufficient.

For:

```text
A student scored 80, 70 and 90.
Calculate the average.
```

Chain-of-Thought provides a structured reasoning approach.

For:

```text
Find the fee of CS101 and then calculate the total fee for 3 students.
```

ReAct is useful because the problem contains both:

1. External information retrieval.
2. Arithmetic.

The ReAct flow can be:

```text
Get CS101 fee
       ↓
Observation = ₹45,000
       ↓
Calculate 45,000 × 3
       ↓
Observation = ₹1,35,000
       ↓
Final Answer
```

This demonstrates why combining reasoning and tools is useful for certain problems.

---

# 10. Transparency

Transparency differs between the approaches.

Direct Prompting provides the final response but does not provide a tool-use process.

Chain-of-Thought can provide a concise explanation of how an answer was obtained, but private internal chain-of-thought should not be exposed.

ReAct provides an observable tool interaction process.

For example:

```text
[ACTION]
get_course_fee("CS101")

[OBSERVATION]
₹45,000
```

This makes the external information retrieval step easier to inspect.

---

# 11. Speed and Cost

Direct Prompting has the simplest flow.

```text
Question → Answer
```

Therefore, it generally has the lowest application-level overhead.

Chain-of-Thought requires more reasoning.

ReAct may require additional model calls and tool calls.

The conceptual overhead is:

```text
Direct Prompting
      ↓
Lowest additional workflow overhead

Chain-of-Thought
      ↓
Additional reasoning

ReAct
      ↓
Reasoning + tool selection + tool execution + observation
```

Therefore, a more capable workflow may also require additional processing.

---

# 12. Self-Consistency Experiment

## 12.1 Objective

The self-consistency experiment tests whether the same reasoning question produces the same answer when executed multiple times at a non-zero temperature.

The experiment uses the following question:

```text
A student has three subjects.

Subject 1 = 80 marks
Subject 2 = 70 marks
Subject 3 = 90 marks

What is the average mark?
```

The correct calculation is:

```text
(80 + 70 + 90) / 3

= 240 / 3

= 80
```

---

## 12.2 Experimental Procedure

The question is run multiple times with:

```text
temperature = 0.7
```

The generated answers are recorded.

The majority answer is then identified.

After that, the same question is run with:

```text
temperature = 0
```

The result is compared with the repeated non-zero-temperature outputs.

---

## 12.3 Observation

The actual output from the experiment should be recorded from the program rather than assumed in advance.

For example, the results can be recorded in this format:

| Run | Answer |
| --- | ------ |
| 1   | 80     |
| 2   | 80     |
| 3   | 80     |
| 4   | 80     |
| 5   | 80     |

Majority answer:

```text
80
```

Temperature-0 answer:

```text
80
```

If the actual program produces different wording or outputs, the recorded screenshot/output should be used as the final experimental evidence.

---

## 12.4 Interpretation

The correct numerical answer to this problem is deterministic because the input values are fixed.

A non-zero temperature can introduce variation in the generated response, particularly in wording or reasoning presentation.

Temperature 0 generally reduces generation variability for the same prompt, although it should not be treated as a universal guarantee of identical behavior in every system.

The important purpose of the experiment is to observe consistency rather than assume it.

---

# 13. Suitability Analysis

The suitability of each approach depends on the type of problem.

## Direct Prompting

Direct prompting is suitable when:

* The question is simple.
* No external information is required.
* A fast response is preferred.
* The model already has the information needed.

Example:

```text
What is 25 + 35?
```

---

## Chain-of-Thought

Chain-of-Thought prompting is suitable when:

* The problem contains multiple reasoning steps.
* All required information is available in the question.
* Careful reasoning is more important than a simple direct response.

Example:

```text
A student scored 80, 70 and 90.
Calculate the average.
```

---

## ReAct

ReAct is suitable when:

* The problem requires external information.
* The problem requires one or more tools.
* The agent needs to combine retrieved information with reasoning.
* The answer depends on current or application-specific data.

Example:

```text
What is the fee for CS101?
```

or:

```text
What is the total fee for three CS101 students?
```

The second question requires both information retrieval and calculation.

---

# 14. Most Suitable Approach for This Scenario

The College Fee Assistant contains both reasoning-only and tool-dependent questions.

Therefore, the approach required depends on the question type.

For a simple calculation, Direct Prompting can be sufficient.

For a multi-step calculation where all information is already provided, Chain-of-Thought can be useful.

For questions requiring the exact course fee stored in the application's tool system, ReAct provides the required tool interaction.

Therefore, the project demonstrates that there is no single approach that should be used for every question. The approach should match the requirements of the problem.

For this particular scenario, ReAct is especially useful for the **tool-dependent part** because the assistant needs to retrieve the course fee before answering.

---

# 15. Limitations

## Direct Prompting Limitations

* No external tool access.
* Cannot retrieve the project's course-fee data.
* Less suitable for complex workflows.

## Chain-of-Thought Limitations

* Does not automatically provide external information.
* Still depends on the information available to the model.
* More reasoning does not replace a required external tool.

## ReAct Limitations

* More complex implementation.
* Requires correct tool selection.
* Requires correct tool arguments.
* Requires interpreting tool observations correctly.
* Additional model/tool calls can increase latency and cost.

---

# 16. General Conclusion

The three approaches provide different capabilities.

**Direct Prompting** is useful for straightforward questions where the model already has the required information. It provides a simple and fast interaction.

**Chain-of-Thought Prompting** is useful for problems that require multiple reasoning steps. It can improve the handling of structured reasoning problems, but reasoning alone cannot retrieve information that is unavailable to the model.

**ReAct** combines reasoning with actions. The agent can identify when external information is needed, call a tool, observe the result, and use that result to produce a final answer.

The general decision can therefore be summarized as:

```text
Simple question
      ↓
Direct Prompting

Multi-step reasoning
      ↓
Chain-of-Thought

Reasoning + external information/tools
      ↓
ReAct
```

The College Fee Assistant demonstrates this distinction clearly. A simple mathematical question can be answered directly, a multi-step calculation can benefit from careful reasoning, and a course-fee question requires access to the course-fee tool.

The self-consistency experiment also demonstrates why repeated model outputs should be observed rather than assuming that every non-zero-temperature run will produce exactly the same response.

Overall, the choice of approach should depend on the requirements of the problem: simplicity, reasoning complexity, external information requirements, speed, and the need for tool interaction.
