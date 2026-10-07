# Day 6 – Robust Agentic AI with Tool Calling

## Campus Event Assistant

A robust Agentic AI system built using **Python, Groq API, OpenAI-compatible Chat Completions, Function Calling, JSON Schema validation, Fault Injection, and Structured Outputs**.

The project demonstrates how an AI agent can decide when to use external tools, execute those tools safely, handle invalid tool calls, recover from failures, and finally provide a natural-language answer to the user.

---

# 1. Project Overview

This project is developed as part of the **Day 6 Agentic AI training task**.

The main objective is to understand how a plain language model becomes an **AI agent** when it is connected to tools and an execution loop.

The project uses a college-campus scenario called:

> **Campus Event Assistant**

The assistant helps students answer questions about campus events.

For example:

- What is the fee for the AI Hackathon?
- Where is the Robotics Workshop?
- What day is the Cultural Fest?
- How much would two AI Hackathon registrations cost?
- What are the fee and venue for the AI Hackathon?
- Can you calculate the total cost for multiple registrations?

The model itself does not directly know the event database.

Instead, the model receives tool definitions and decides when a tool is required.

The Python application then:

1. Receives the user's question.
2. Sends the question and tool definitions to the model.
3. Checks whether the model requested a tool.
4. Parses the tool arguments.
5. Finds the requested tool.
6. Validates the arguments.
7. Executes the tool.
8. Sends the tool result back to the model.
9. Allows the model to continue reasoning.
10. Returns the final answer to the user.

This creates the basic agentic loop:

```text
User
  |
  v
AI Model
  |
  | tool call
  v
Python Agent
  |
  +--> Parse JSON
  |
  +--> Look up Tool
  |
  +--> Validate Arguments
  |
  +--> Execute Tool
  |
  v
Tool Result
  |
  v
AI Model
  |
  v
Final Answer
```

---

# 2. Why This Project Is Agentic

A normal chatbot only generates text.

For example:

```text
User:
What is the fee for the AI Hackathon?

Chatbot:
The fee is probably ₹300.
```

The problem is that the chatbot may guess.

Our agent is different.

It has access to a real Python tool:

```text
get_event_info()
```

The model can request:

```json
{
    "event_name": "AI_HACKATHON",
    "detail": "fee"
}
```

The Python application executes the tool and obtains the actual value:

```text
300
```

The result is then sent back to the model.

The model can finally answer:

```text
The AI Hackathon registration fee is ₹300.
```

Therefore:

```text
Agent = LLM + Tools + Loop
```

The model decides **what should happen**, while the application controls **what is actually executed**.

---

# 3. Scenario

## Campus Event Assistant

The scenario contains three college events.

| Event | Fee | Day | Venue | Category |
|---|---:|---|---|---|
| AI_HACKATHON | ₹300 | Saturday | Innovation Lab | Technical |
| ROBOTICS_WORKSHOP | ₹250 | Friday | Robotics Lab | Technical |
| CULTURAL_FEST | ₹150 | Monday | Main Auditorium | Cultural |

The assistant has two tools.

### Tool 1 – `get_event_info`

This tool retrieves information about a campus event.

It can provide:

- Fee
- Day
- Venue
- Category

### Tool 2 – `calculate_cost`

This tool performs safe arithmetic.

Example:

```text
300 * 2
```

Result:

```text
600
```

Another example:

```text
300 * 2 + 150
```

Result:

```text
750
```

The calculator does not use unrestricted Python `eval()`.

Instead, it parses the expression using Python's `ast` module and only allows:

```text
+
-
*
/
()
```

This prevents arbitrary Python code from being executed.

---

# 4. Features Implemented

This project demonstrates the following concepts:

- Groq API
- OpenAI-compatible API
- Chat Completions
- Function/tool calling
- JSON Schema
- Tool descriptions
- Required arguments
- Enum validation
- `additionalProperties: false`
- Tool choice
- Parallel tool calls
- Tool-call loop
- Tool result messages
- `tool_call_id`
- JSON argument parsing
- Runtime validation
- Unknown tool handling
- Missing argument handling
- Wrong type handling
- Invalid enum handling
- Invented argument handling
- Unknown event handling
- Invalid calculator expression handling
- Truncated response handling
- Repeated tool-call protection
- Maximum-step protection
- Fault injection
- Structured output
- JSON mode
- JSON Schema mode
- Error recovery
- Defensive agent design

---

# 5. Technologies Used

## Programming Language

Python 3

## API Provider

Groq API

## Model

Default model:

```text
openai/gpt-oss-20b
```

The model can be changed through the `.env` file.

Example:

```env
GROQ_MODEL=openai/gpt-oss-20b
```

## Python Libraries

```text
openai
python-dotenv
```

The OpenAI Python client is used with Groq's OpenAI-compatible endpoint.

---

# 6. Project Structure

```text
day6_lab/
│
├── .env
├── .gitignore
├── requirements.txt
│
├── tools_v2.py
├── validate.py
├── robust_agent.py
├── inject_faults.py
├── structured_demo.py
│
├── screenshots/
│   ├── validator_output.png
│   ├── fault_injection.png
│   ├── single_tool.png
│   ├── parallel_tools.png
│   ├── invalid_value.png
│   ├── no_tool.png
│   └── structured_output.png
│
├── README.md
└── analysis.md
```

---

# 7. File Description

## `tools_v2.py`

Contains:

- Campus event data
- `get_event_info()`
- `calculate_cost()`
- Tool implementations
- Tool definitions
- JSON Schemas
- Shared `SCHEMAS` dictionary

The important design decision is that the same schemas are reused by both:

1. The model/tool definition
2. The local validator

This avoids having two different definitions of what a valid tool call looks like.

---

## `validate.py`

Contains the runtime argument validator.

It checks:

- Required arguments
- Argument types
- Enum values
- Extra arguments

The validator runs before the actual Python function is executed.

Therefore, a model-generated argument is treated as **untrusted input**.

---

## `robust_agent.py`

Contains the main agent.

It implements:

- Groq API connection
- Chat Completions
- Tool calling
- Tool-call loop
- JSON parsing
- Tool lookup
- Schema validation
- Tool execution
- Parallel tool-call handling
- Retry after `length`
- Repeated-call protection
- Maximum-step protection

---

## `inject_faults.py`

Tests the tool-handling system without using the model.

It manually creates broken tool calls.

Examples:

- Invalid JSON
- Unknown tool
- Missing argument
- Wrong type
- Invalid enum
- Extra argument
- Unknown event
- Unsafe calculator expression
- Empty arguments

This demonstrates defensive programming.

---

## `structured_demo.py`

Runs the same extraction problem in three different ways:

1. No constraint
2. JSON mode
3. JSON Schema mode

This demonstrates the difference between ordinary text generation, JSON output, and schema-constrained output.

---

# 8. Installation

## Step 1 – Create a virtual environment

Open PowerShell in the project folder.

Run:

```powershell
python -m venv .venv
```

---

## Step 2 – Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the script, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then:

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see something similar to:

```text
(.venv)
```

at the beginning of the terminal line.

---

# 9. Install Dependencies

Run:

```powershell
pip install -r requirements.txt
```

The required packages are:

```text
openai
python-dotenv
```

---

# 10. Configure Groq API

Create a file named:

```text
.env
```

Add:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

Replace:

```text
your_groq_api_key_here
```

with your actual Groq API key.

Example:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxx
GROQ_MODEL=openai/gpt-oss-20b
```

Do not share the API key publicly.

---

# 11. Environment Variable Security

The `.env` file contains a private API key.

Therefore it must NOT be pushed to GitHub.

The `.gitignore` file contains:

```gitignore
.env
.env.*
```

Therefore Git will ignore the API key file.

Never write the API key directly inside:

```text
robust_agent.py
structured_demo.py
```

Use environment variables instead.

---

# 12. Running the Project

## Test the tool definitions

Run:

```powershell
python tools_v2.py
```

Expected output will show:

```text
CAMPUS EVENT ASSISTANT - AVAILABLE TOOLS
```

and the available events and tools.

---

# 13. Test the Validator

Run:

```powershell
python validate.py
```

The validator tests valid and invalid arguments.

Examples:

```text
{'event_name': 'AI_HACKATHON'} -> OK

{} -> Missing required argument

{'event_name': 101} -> Argument must be a string

{'event_name': 'AI_HACKATHON', 'detail': 'price'}
-> Argument must be one of the allowed values
```

---

# 14. Run Fault Injection

Run:

```powershell
python inject_faults.py
```

This test does NOT need the model.

It does NOT make an API call.

It directly tests the tool-handling layer.

Example categories:

```text
good call
invalid JSON
unknown tool
missing required argument
wrong type
value outside enum
invented extra argument
unknown event
unsafe calculator expression
empty arguments
```

The important property is that the handler returns an error as a **string** instead of crashing the application.

---

# 15. Run the Robust Agent

Run:

```powershell
python robust_agent.py
```

The agent sends questions to Groq.

Example questions:

```text
What is the fee for the AI Hackathon?

What are the fee and venue for the AI Hackathon?

How much would 2 AI Hackathon registrations cost?

What is the fee for the Robotics Competition?

Write a one-line welcome message for a new student.
```

---

# 16. Example Agent Flow

Suppose the user asks:

```text
What is the fee for the AI Hackathon?
```

The model may decide that it needs:

```text
get_event_info
```

with:

```json
{
    "event_name": "AI_HACKATHON",
    "detail": "fee"
}
```

The application then:

```text
1. Parses JSON
2. Finds get_event_info
3. Validates the arguments
4. Executes get_event_info
```

The tool returns:

```text
300
```

The application sends:

```text
role = tool
tool_call_id = <original call id>
content = 300
```

The model then produces:

```text
The AI Hackathon registration fee is ₹300.
```

---

# 17. Tool Calling Lifecycle

The complete lifecycle is:

```text
Step 1
User asks a question
        |
        v
Step 2
Application sends:
- messages
- tools
- tool schemas
        |
        v
Step 3
Model decides whether a tool is required
        |
        v
Step 4
Model returns tool_calls
        |
        v
Step 5
Application parses arguments
        |
        v
Step 6
Application looks up tool
        |
        v
Step 7
Application validates arguments
        |
        v
Step 8
Application executes tool
        |
        v
Step 9
Application sends tool result
        |
        v
Step 10
Model generates final answer
```

---

# 18. Why Tool Calls Must Be Treated as Untrusted

The model is generating the arguments.

For example, it might generate:

```json
{
    "event_name": "SPORTS_DAY"
}
```

even though the event does not exist.

Or:

```json
{
    "event_name": 123
}
```

instead of a string.

Or:

```json
{
    "event_name": "AI_HACKATHON",
    "year": 2026
}
```

where `year` is not part of the tool schema.

Therefore:

> Model output should never be treated as trusted program input.

The application must validate it before executing anything.

---

# 19. JSON Schema Used in the Project

The event tool contains:

```json
{
    "type": "object",
    "properties": {
        "event_name": {
            "type": "string",
            "enum": [
                "AI_HACKATHON",
                "ROBOTICS_WORKSHOP",
                "CULTURAL_FEST"
            ]
        },
        "detail": {
            "type": "string",
            "enum": [
                "fee",
                "day",
                "venue",
                "category"
            ]
        }
    },
    "required": [
        "event_name"
    ],
    "additionalProperties": false
}
```

Important parts:

### `type`

Defines the expected JSON type.

Example:

```json
"type": "string"
```

---

### `properties`

Defines the allowed arguments.

---

### `enum`

Restricts a value to a fixed set.

Example:

```json
"enum": [
    "AI_HACKATHON",
    "ROBOTICS_WORKSHOP",
    "CULTURAL_FEST"
]
```

---

### `required`

Specifies arguments that must be present.

Example:

```json
"required": [
    "event_name"
]
```

---

### `additionalProperties`

The project uses:

```json
"additionalProperties": false
```

This prevents invented arguments.

For example:

```json
{
    "event_name": "AI_HACKATHON",
    "year": 2026
}
```

should be rejected because `year` is not defined.

---

# 20. Tool Choice

The Chat Completions API supports different tool-selection behaviors.

Conceptually:

```text
auto
none
required
named tool
```

### `auto`

The model decides whether a tool is needed.

This is used in the main agent:

```python
tool_choice="auto"
```

---

### `none`

The model should not use tools.

---

### `required`

The model must use a tool.

---

### Named tool

The application can request a particular tool.

For example, conceptually:

```text
get_event_info
```

This is useful when the application knows exactly which tool should be used.

---

# 21. Parallel Tool Calls

A model may request more than one tool call in a single response.

For example:

```text
What are the fee and venue for the AI Hackathon?
```

The model may request:

```text
Call 1:
get_event_info(
    event_name="AI_HACKATHON",
    detail="fee"
)

Call 2:
get_event_info(
    event_name="AI_HACKATHON",
    detail="venue"
)
```

These are independent operations.

The application must loop over **all** tool calls.

It must not process only the first one.

For every tool call, it must return exactly one corresponding tool message using:

```text
tool_call_id
```

This is important because the model uses the ID to associate each result with the correct request.

---

# 22. Handling `finish_reason`

The agent checks the model's:

```text
finish_reason
```

Important cases include:

## `stop`

The model has completed its response.

The application can return the final answer.

---

## `tool_calls`

The model wants one or more tools to be executed.

The application must:

1. Append the assistant tool-call message.
2. Execute every tool call.
3. Append one tool message per `tool_call_id`.
4. Send the updated conversation back to the model.
5. Continue the loop.

---

## `length`

The response was stopped because the token limit was reached.

The project responds by increasing:

```python
max_tokens
```

and retrying.

For example:

```text
500
```

becomes:

```text
1000
```

and then:

```text
2000
```

if required.

---

# 23. Why `message.content` Can Be Empty

When the model wants to call a tool, the assistant message may contain tool calls instead of normal text.

Therefore:

```python
message.content
```

can be empty or `None`.

The important information may instead be:

```python
message.tool_calls
```

The agent therefore checks:

```python
if not message.tool_calls:
    return message.content
```

instead of assuming that every assistant response contains normal text.

---

# 24. Error Handling

The project handles several classes of errors.

## Invalid JSON

Example:

```text
{"event_name": "AI_HACKATHON"
```

The JSON is incomplete.

The agent returns a string describing the problem.

---

## Unknown Tool

Example:

```text
send_email
```

The application checks whether the name exists in:

```python
TOOL_FUNCTIONS
```

If not, it returns an error.

---

## Missing Argument

Example:

```json
{}
```

The required:

```text
event_name
```

is missing.

---

## Wrong Type

Example:

```json
{
    "event_name": 101
}
```

The schema expects a string.

---

## Invalid Enum

Example:

```json
{
    "event_name": "SPORTS_DAY"
}
```

`SPORTS_DAY` is not one of the allowed event names.

---

## Invented Argument

Example:

```json
{
    "event_name": "AI_HACKATHON",
    "year": 2026
}
```

The `year` argument is not defined.

Because the schema contains:

```json
"additionalProperties": false
```

the validator rejects it.

---

## Invalid Calculator Expression

Example:

```text
__import__('os').system('dir')
```

The calculator does not allow arbitrary Python expressions.

The AST evaluator rejects unsupported syntax.

---

# 25. Repair Pattern

The project follows an important repair pattern:

> Every tool-handling stage returns a string.

For example:

```text
Argument error: Missing required argument 'event_name'.
```

or:

```text
Unknown tool: send_email.
```

or:

```text
Calculator error: Unsupported expression.
```

This means the agent does not immediately crash.

The error can become part of the tool result sent back to the model.

The model can then potentially recover.

This is safer than allowing an exception to terminate the complete agent loop.

---

# 26. Repeated Tool Call Protection

An AI agent can sometimes repeatedly request the same tool with the same arguments.

For example:

```text
Call:
get_event_info(AI_HACKATHON)

Call:
get_event_info(AI_HACKATHON)

Call:
get_event_info(AI_HACKATHON)
```

If this continues forever, the application could waste API calls.

The project stores previously seen calls:

```python
seen
```

and stops when an identical call reaches the configured limit.

The project also has:

```python
max_steps
```

to prevent an infinite agent loop.

---

# 27. Fault Injection

Fault injection is implemented in:

```text
inject_faults.py
```

The important point is:

> The fault injection test does not use the model.

It manually constructs fake tool calls.

This makes testing:

- Fast
- Repeatable
- Offline
- Independent of model behavior
- Useful for debugging

The test includes at least eight broken cases.

Examples:

| Fault | Expected Handling |
|---|---|
| Invalid JSON | Return error string |
| Unknown tool | Return error string |
| Missing argument | Validator rejects |
| Wrong type | Validator rejects |
| Invalid enum | Validator rejects |
| Extra argument | Validator rejects |
| Unknown event | Tool returns error |
| Unsafe expression | Calculator rejects |
| Empty arguments | Validation/tool handling catches issue |

---

# 28. Structured Output

The project also compares three output modes.

The same extraction question is used:

```text
I want to join the AI Hackathon on Saturday
with a student pass and bring 2 guests.
```

The program asks the model to extract:

```text
event_name
day
pass_type
guest_count
```

in three ways.

---

## Mode 1 – No Constraint

The model is simply asked to extract the information.

The model may respond in normal text.

Example:

```text
The event is AI_HACKATHON, the day is Saturday,
the pass type is student, and there are 2 guests.
```

This is readable but not necessarily convenient for a program to consume.

---

## Mode 2 – JSON Mode

The model is requested to return JSON.

Example:

```json
{
    "event_name": "AI_HACKATHON",
    "day": "Saturday",
    "pass_type": "student",
    "guest_count": 2
}
```

JSON mode improves machine readability.

However, valid JSON does not automatically guarantee that every value is correct.

For example:

```json
{
    "event_name": "AI_HACKATHON",
    "guest_count": "two"
}
```

could have the wrong type if the provider/model is not enforcing a schema.

---

## Mode 3 – JSON Schema Mode

The project supplies a JSON Schema.

The required fields and types are explicitly defined.

Example:

```json
{
    "type": "object",
    "properties": {
        "event_name": {
            "type": "string"
        },
        "day": {
            "type": "string"
        },
        "pass_type": {
            "type": "string"
        },
        "guest_count": {
            "type": "integer"
        }
    },
    "required": [
        "event_name",
        "day",
        "pass_type",
        "guest_count"
    ],
    "additionalProperties": false
}
```

This provides stronger structural guarantees.

---

# 29. Tool Calling vs Structured Outputs

| Feature | Tool Calling | Structured Outputs |
|---|---|---|
| Main purpose | Ask application to perform an action | Force response into a schema |
| Produces | Tool request | Structured data |
| Application executes something | Yes | Not necessarily |
| Useful for external functions | Yes | No |
| Useful for extraction | Sometimes | Yes |
| Uses JSON Schema | Yes | Yes |
| Example | `get_event_info()` | Extract event details |
| Agent loop | Usually | Usually not required |
| Main goal | Action | Reliable data shape |

The two concepts solve different problems.

Tool calling answers:

> "What should the application execute?"

Structured output answers:

> "What shape should the model's answer have?"

---

# 30. Security Considerations

The application does not blindly trust model-generated arguments.

It validates:

```text
JSON syntax
      |
      v
Tool existence
      |
      v
Required fields
      |
      v
Data types
      |
      v
Enum values
      |
      v
Extra fields
      |
      v
Tool execution
```

The calculator also avoids unrestricted:

```python
eval()
```

and instead uses an AST-based safe evaluator.

This is an important safety property.

---

# 31. Screenshots

The following screenshots should be added to the repository:

```text
screenshots/
├── validator_output.png
├── fault_injection.png
├── single_tool.png
├── parallel_tools.png
├── invalid_value.png
├── no_tool.png
└── structured_output.png
```

Recommended screenshots:

### `validator_output.png`

Show:

```powershell
python validate.py
```

---

### `fault_injection.png`

Show:

```powershell
python inject_faults.py
```

---

### `single_tool.png`

Show a question such as:

```text
What is the fee for the AI Hackathon?
```

and the tool call/result.

---

### `parallel_tools.png`

Show:

```text
What are the fee and venue for the AI Hackathon?
```

and ideally two tool calls.

---

### `invalid_value.png`

Show either:

- an actual model-generated invalid value, if it occurs, or
- the fault injection test for invalid enum values.

Do not claim that the model generated an invalid value if it did not.

---

### `no_tool.png`

Show a question that does not require a tool:

```text
Write a one-line welcome message for a new student.
```

---

### `structured_output.png`

Show the output from:

```powershell
python structured_demo.py
```

including:

```text
NO CONSTRAINT
JSON MODE
JSON SCHEMA MODE
```

---

# 32. Important Observation

The invalid-value test must distinguish between:

### Model behavior

The model may correctly follow the provided schema and never generate an invalid enum.

### Fault injection

The application can still be tested with an intentionally invalid enum.

Therefore, if the model never generates an invalid event value, the correct observation is:

```text
The invalid enum was not observed during the normal model run.
The same failure was deliberately tested using fault injection.
```

This is better than inventing a model failure.

---

# 33. How the Project Demonstrates Agentic Behavior

The project demonstrates agentic behavior through:

```text
Decision
  ↓
Tool Selection
  ↓
Tool Execution
  ↓
Observation
  ↓
Next Decision
  ↓
Final Answer
```

The model is not simply generating one answer.

It participates in a loop where the result of one operation can influence what happens next.

---

# 34. Limitations

This is an educational implementation.

It does not implement:

- Database persistence
- User authentication
- Real college event registration
- Payment processing
- Production monitoring
- Distributed execution
- Human approval workflows
- Long-term memory

The event data is stored locally in Python.

---

# 35. Future Improvements

Possible improvements include:

1. Connect the event tool to a real database.
2. Add event registration.
3. Add seat availability.
4. Add student authentication.
5. Add payment integration.
6. Add email confirmation.
7. Add logging.
8. Add retry backoff.
9. Add unit tests.
10. Add a web interface.
11. Add conversation memory.
12. Add human approval before important actions.
13. Add database transactions.
14. Add monitoring and tracing.
15. Add more tools.

---

# 36. Learning Outcomes

After completing this project, the following concepts are demonstrated:

- What an AI agent is
- Difference between chatbot and agent
- Tool/function calling
- JSON Schema
- API orchestration
- OpenAI-compatible APIs
- Groq integration
- Chat Completions
- Parallel tool calls
- Tool-call IDs
- Agent loops
- Runtime validation
- Error handling
- Fault injection
- Structured outputs
- JSON mode
- Schema mode
- Defensive programming

---

# 37. Conclusion

The Campus Event Assistant demonstrates that building an AI agent is not only about sending a prompt to a language model.

A reliable agent requires an orchestration layer around the model.

The model can decide which tool it wants to use, but the application must:

- Parse the request
- Validate the arguments
- Verify the tool
- Execute only approved operations
- Return every tool result
- Handle failures
- Prevent infinite loops
- Retry truncated responses
- Produce a final answer

The main lesson is:

> **Model-generated tool calls are untrusted input.**

JSON Schema can strongly constrain the structure of the request, but application-level validation is still important.

The project therefore combines:

```text
LLM
+
Tools
+
JSON Schema
+
Validation
+
Execution
+
Error Handling
+
Loop Control
```

to create a more reliable Agentic AI system.

---

# 38. Quick Start

After setting up `.env`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python tools_v2.py
python validate.py
python inject_faults.py
python robust_agent.py
python structured_demo.py
```

---

# 39. GitHub Submission Checklist

Before pushing the project:

- [ ] `tools_v2.py`
- [ ] `validate.py`
- [ ] `robust_agent.py`
- [ ] `inject_faults.py`
- [ ] `structured_demo.py`
- [ ] `requirements.txt`
- [ ] `.gitignore`
- [ ] `README.md`
- [ ] `analysis.md`
- [ ] `screenshots/`
- [ ] `.env` is NOT pushed
- [ ] API key is NOT visible in screenshots
- [ ] All Python files run successfully
- [ ] Fault injection works without API
- [ ] Structured output demo works
- [ ] Screenshots are added
- [ ] GitHub repository is updated

---

# 40. Final Project Structure

```text
Day6/
│
├── .env                  # Local only - DO NOT PUSH
├── .gitignore
├── requirements.txt
│
├── tools_v2.py
├── validate.py
├── robust_agent.py
├── inject_faults.py
├── structured_demo.py
│
├── screenshots/
│   ├── validator_output.png
│   ├── fault_injection.png
│   ├── single_tool.png
│   ├── parallel_tools.png
│   ├── invalid_value.png
│   ├── no_tool.png
│   └── structured_output.png
│
├── README.md
└── analysis.md
```

---

## Author

**Manoranjith M**

Day 6 – Agentic AI Training

Project: **Campus Event Assistant**