# Day 6 Analysis – Robust Agentic AI with Tool Calling

## Campus Event Assistant

---

# 1. Introduction

This project demonstrates how a language model can be connected to external tools to create an Agentic AI system.

Instead of allowing the language model to answer every question from its own generated knowledge, the application gives the model access to controlled tools.

The selected scenario is a:

> **Campus Event Assistant**

The assistant provides information about college events and performs simple registration-cost calculations.

The project contains two tools:

1. `get_event_info`
2. `calculate_cost`

The system is implemented using the Groq API through an OpenAI-compatible Chat Completions interface.

The main purpose of this analysis is to understand:

- How Chat Completions works
- How tool calling works
- Why model-generated tool calls must be treated as untrusted
- How JSON Schema constrains tool arguments
- How parallel tool calls are handled
- How an agent loop works
- How failures are detected and repaired
- How fault injection can test the system without a model
- The difference between tool calling and structured outputs
- When structured outputs are more suitable than tool calling

---

# 2. Scenario

The Campus Event Assistant contains the following event information.

| Event | Fee | Day | Venue | Category |
|---|---:|---|---|---|
| AI_HACKATHON | ₹300 | Saturday | Innovation Lab | Technical |
| ROBOTICS_WORKSHOP | ₹250 | Friday | Robotics Lab | Technical |
| CULTURAL_FEST | ₹150 | Monday | Main Auditorium | Cultural |

The assistant provides two tools.

## Tool 1: `get_event_info`

This tool returns:

- fee
- day
- venue
- category

for a valid campus event.

## Tool 2: `calculate_cost`

This tool performs basic arithmetic.

For example:

```text
300 * 2
```

returns:

```text
600
```

The calculator is implemented using Python's AST module instead of unrestricted `eval()`.

Only basic arithmetic operators are accepted.

---

# 3. Chat Completions Analysis

## 3.1 Important Request Fields

The main agent uses a Chat Completions request.

The important request fields are:

```python
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=TOOLS,
    tool_choice="auto",
    parallel_tool_calls=True,
    temperature=0,
    max_tokens=max_tokens,
)
```

Each field has a specific purpose.

---

## `model`

The `model` field specifies which language model should process the request.

The project uses:

```text
openai/gpt-oss-20b
```

The model is stored in `.env` so that it can be changed without modifying the Python source code.

Example:

```env
GROQ_MODEL=openai/gpt-oss-20b
```

---

## `messages`

The `messages` array contains the conversation.

It can include:

```text
system
user
assistant
tool
```

messages.

For example:

```python
messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    },
    {
        "role": "user",
        "content": question
    }
]
```

After a tool call, the conversation is extended with:

```text
assistant tool-call message
+
tool result messages
```

This allows the model to see the result of the tool it requested.

---

## `tools`

The `tools` field provides the model with the available functions.

The model does not automatically know the Python implementation.

It only receives the tool description and its schema.

For example:

```text
get_event_info
```

is described using JSON Schema.

The model can then decide whether that tool is appropriate.

---

## `tool_choice`

The project uses:

```python
tool_choice="auto"
```

This means the model can decide whether to call a tool.

Other common choices include:

```text
auto
none
required
specific named tool
```

`auto` is useful for this project because some questions require tools while others do not.

---

## `temperature`

The project uses:

```python
temperature=0
```

A lower temperature is useful for this task because we want predictable tool selection and consistent outputs.

---

## `max_tokens`

The `max_tokens` value limits how much output can be generated.

The project starts with:

```python
max_tokens = 500
```

If the API reports:

```text
finish_reason = length
```

the project increases the token budget and retries.

This demonstrates handling of truncated responses.

---

## `parallel_tool_calls`

The project uses:

```python
parallel_tool_calls=True
```

This allows the model to request multiple independent tool calls in one response when supported.

For example:

```text
What are the fee and venue for the AI Hackathon?
```

may produce two calls:

```text
get_event_info(fee)
get_event_info(venue)
```

The application loops over all returned calls.

---

## `response_format`

The structured-output demonstration uses:

```python
response_format
```

instead of tool calling.

Three modes are compared:

```text
No constraint
JSON mode
JSON Schema mode
```

JSON Schema mode provides stronger structural constraints than ordinary JSON mode.

---

# 4. Important Response Fields

A Chat Completions response contains information such as:

```text
id
choices
message
finish_reason
usage
```

The project mainly uses:

```python
response.choices[0]
```

and then:

```python
choice.message
choice.finish_reason
```

---

## `id`

The response ID identifies the generated completion.

---

## `choices`

The API returns one or more choices.

The project uses the first choice:

```python
response.choices[0]
```

---

## `message`

The message contains the assistant response.

It may contain:

```text
content
tool_calls
```

When a tool call is generated, `content` may be empty while `tool_calls` contains the important information.

Therefore, an application should not assume that every assistant message contains normal text.

---

## `finish_reason`

The `finish_reason` explains why generation stopped.

The project focuses on:

```text
stop
length
tool_calls
```

---

## `usage`

Usage information can provide token-related information about the request and response.

This is useful for monitoring API usage and understanding how much model output is being consumed.

---

# 5. Understanding `finish_reason`

## 5.1 `stop`

When:

```text
finish_reason = stop
```

the model has completed the response.

If there are no tool calls, the application can return the generated content to the user.

---

## 5.2 `length`

When:

```text
finish_reason = length
```

the generation reached its token limit.

The project responds by increasing:

```python
max_tokens
```

and retrying.

The logic is approximately:

```text
500
 ↓
1000
 ↓
2000
```

The exact number of retries is limited.

This prevents the application from retrying forever.

---

## 5.3 `tool_calls`

When the model wants to use a tool, it can return:

```text
finish_reason = tool_calls
```

with a `tool_calls` array.

The application must then:

1. Save the assistant tool-call message.
2. Process every tool call.
3. Execute the appropriate functions.
4. Create one tool message for every call.
5. Match every result using `tool_call_id`.
6. Send the updated conversation back to the model.
7. Continue until a final answer is produced.

---

# 6. Why `message.content` Can Be Empty

A tool-call response is not necessarily a normal text response.

For example:

```text
assistant
tool_calls:
    get_event_info(...)
```

In such a response:

```python
message.content
```

may be empty.

The important information is:

```python
message.tool_calls
```

Therefore, the agent first checks whether tool calls exist.

---

# 7. OpenAI-Compatible APIs

The project uses the OpenAI Python client but sends requests to Groq.

The important configuration is:

```python
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)
```

This means the Python code can use the OpenAI client's familiar API style while the actual model request is sent to Groq.

Groq describes this as OpenAI compatibility, while also noting that compatibility does not mean every OpenAI feature is identical or supported. :contentReference[oaicite:1]{index=1}

The important provider-specific changes are:

```text
API key
+
base URL
+
model name
```

The application logic remains largely the same.

---

# 8. Why API Compatibility Is Useful

OpenAI-compatible APIs reduce the amount of application code that must change when switching providers.

For example, the application can use:

```python
client.chat.completions.create(...)
```

while changing:

```python
base_url
```

and:

```python
model
```

This makes experimentation with different providers easier.

However, compatibility should not be interpreted as:

> Every feature behaves exactly the same on every provider.

The application should always check the provider's current model and API documentation before depending on a particular feature.

---

# 9. Streaming

Streaming means that model output is delivered incrementally rather than waiting for the complete response.

Without streaming:

```text
Request
   ↓
Wait
   ↓
Complete response
```

With streaming:

```text
Request
   ↓
Token 1
Token 2
Token 3
Token 4
...
```

Streaming is useful for:

- Faster perceived response time
- Chat interfaces
- Long responses
- Real-time user interfaces

However, agentic tool loops require additional care.

The application needs the complete tool-call information before it can safely execute the requested tool.

Therefore, for this educational project, normal non-streaming Chat Completions are simpler.

The project focuses on understanding the complete tool-call lifecycle instead of streaming UI behavior.

---

# 10. Responses API vs Chat Completions

Modern AI APIs can provide different interfaces for model interaction.

The project intentionally uses:

```text
Chat Completions
```

because the assignment focuses on understanding:

```text
messages
tool_calls
tool_call_id
finish_reason
```

Chat Completions represents conversation history through messages.

The Responses API uses a more modern item-based interaction model and supports broader orchestration patterns.

For this assignment, Chat Completions is easier to inspect because the tool-call loop is explicit.

Therefore:

```text
This project uses Chat Completions intentionally.
```

The provider currently documents both Chat Completions and a Responses API. :contentReference[oaicite:2]{index=2}

---

# 11. Five Steps of Tool Calling

The complete tool-calling process can be explained in five major steps.

## Step 1 – Define Tools and Send the User Message

The application provides:

```text
messages
+
tools
+
tool schemas
```

to the model.

---

## Step 2 – Model Generates a Tool Call

The model decides that a tool is necessary.

For example:

```json
{
    "name": "get_event_info",
    "arguments": {
        "event_name": "AI_HACKATHON",
        "detail": "fee"
    }
}
```

The actual API representation contains the arguments as JSON text.

---

## Step 3 – Application Parses and Validates

The application performs:

```text
Parse JSON
     ↓
Find tool
     ↓
Validate schema
```

This is critical because model output is not trusted application input.

---

## Step 4 – Execute the Tool

After successful validation:

```python
function(**arguments)
```

is executed.

The result might be:

```text
300
```

---

## Step 5 – Return Tool Result to Model

The application sends:

```text
role = tool
tool_call_id = original ID
content = result
```

The model receives the observation and generates the final answer.

This creates the agent loop:

```text
Think/decide
    ↓
Tool
    ↓
Observation
    ↓
Think/decide again
    ↓
Final answer
```

---

# 12. Why Model Output Is Untrusted

The model generates text and structured tool-call arguments.

Even if the model is highly capable, it should not be considered a trusted program.

Possible problems include:

```text
Invalid JSON
Unknown tool
Missing argument
Wrong type
Invalid enum
Extra argument
Wrong semantic value
Repeated call
Truncated output
```

For example:

```json
{
    "event_name": "AI_HACKATHON",
    "year": 2026
}
```

contains a valid JSON object but also contains an argument that the tool does not support.

Therefore:

> Valid JSON does not mean valid tool input.

The application must perform its own validation.

---

# 13. Tool Definition Components

The project uses JSON Schema to describe tool arguments.

Important components include:

## Description

The tool description helps the model understand when the tool should be used.

Example:

```text
Get information about one campus event.
```

A clearer description generally helps tool selection.

---

## Properties

`properties` defines the available arguments.

Example:

```json
"event_name": {
    "type": "string"
}
```

---

## Enum

`enum` restricts values.

Example:

```json
"enum": [
    "AI_HACKATHON",
    "ROBOTICS_WORKSHOP",
    "CULTURAL_FEST"
]
```

This is useful when only a fixed set of values is valid.

---

## Required

`required` identifies arguments that must exist.

Example:

```json
"required": [
    "event_name"
]
```

---

## `additionalProperties`

The project uses:

```json
"additionalProperties": false
```

This prevents extra fields from being accepted.

For example:

```json
{
    "event_name": "AI_HACKATHON",
    "random_value": "hello"
}
```

should fail validation.

---

## Strict

Strict schema behavior means that supported structured-output/tool mechanisms can enforce the defined structure more strongly.

For structured outputs, Groq currently documents strict mode for supported models and requires stricter schema conditions such as required fields and `additionalProperties: false`. :contentReference[oaicite:3]{index=3}

The main tool schema in this project focuses on explicit validation through the application's own validator.

This is important because application-level validation remains useful even when the provider offers schema constraints.

---

# 14. Tool Choice Modes

The main agent uses:

```python
tool_choice="auto"
```

This allows the model to decide.

Conceptually, the available modes are:

| Mode | Meaning |
|---|---|
| `auto` | Model decides whether to use a tool |
| `none` | No tool should be called |
| `required` | A tool call is required |
| Named tool | Request a particular tool |

---

# 15. JSON Mode vs JSON Schema Mode

These two concepts should not be confused.

## JSON Mode

JSON mode attempts to make the response valid JSON.

The main benefit is:

```text
Machine-readable JSON
```

However:

```text
Valid JSON
≠
Correct data
```

For example:

```json
{
    "event_name": "AI_HACKATHON",
    "guest_count": "many"
}
```

may be valid JSON but violate the desired integer type.

---

## JSON Schema Mode

JSON Schema mode provides a specific expected structure.

For example:

```json
{
    "event_name": "AI_HACKATHON",
    "day": "Saturday",
    "pass_type": "student",
    "guest_count": 2
}
```

The schema defines:

```text
event_name -> string
day -> string
pass_type -> enum/string
guest_count -> integer
```

This is stronger than simply saying:

> "Return JSON."

Groq documents JSON Object Mode and JSON Schema Structured Outputs separately, with JSON Schema being the stronger structured approach on supported models. :contentReference[oaicite:4]{index=4}

---

# 16. Tools vs Structured Outputs

| Aspect | Tool Calling | Structured Outputs |
|---|---|---|
| Main purpose | Request an application action | Produce data in a fixed shape |
| Model requests external operation | Yes | No |
| Python function execution | Yes | Not required |
| JSON Schema | Used for arguments | Used for response structure |
| Agent loop | Common | Not necessarily needed |
| Example | Get event fee | Extract registration details |
| Main question | "What tool should I call?" | "What should the output look like?" |

Tool calling is appropriate when the model needs something performed.

Structured output is appropriate when the application needs a predictable data structure.

---

# 17. Parallel Tool Calls

Parallel tool calling occurs when multiple independent operations can be requested together.

Example user question:

```text
What are the fee and venue for the AI Hackathon?
```

Possible tool calls:

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

The agent must not assume:

```text
only one tool call
```

Instead:

```python
for call in message.tool_calls:
```

is used.

For every call, the application produces:

```python
{
    "role": "tool",
    "tool_call_id": call.id,
    "content": result
}
```

Groq's local tool-calling documentation similarly describes looping over tool calls and returning a tool result associated with each `tool_call_id`. :contentReference[oaicite:5]{index=5}

---

# 18. Why Every `tool_call_id` Must Be Answered

Suppose the model returns:

```text
call_1
call_2
```

If the application only returns:

```text
call_1 -> result
```

then:

```text
call_2
```

has no corresponding tool result.

The conversation state is incomplete.

Therefore:

```text
Number of tool calls
=
Number of corresponding tool messages
```

for the tool calls being handled.

This is one of the most important orchestration rules in the project.

---

# 19. Error Categories Tested

The project deliberately tests several failure types.

| Error | Example | Handling |
|---|---|---|
| Invalid JSON | Broken JSON string | Return error string |
| Unknown tool | `send_email` | Reject |
| Missing argument | `{}` | Validator rejects |
| Wrong type | `event_name: 101` | Validator rejects |
| Invalid enum | `detail: price` | Validator rejects |
| Extra argument | `year: 2026` | Validator rejects |
| Unknown event | `SPORTS_DAY` | Tool returns error |
| Unsafe expression | `__import__...` | Calculator rejects |
| Empty arguments | `""` | Parsing/validation handles |
| Truncated response | `length` | Increase token limit |
| Repeated calls | Same call repeatedly | Stop agent |

---

# 20. Repair Pattern

The agent follows this design:

```text
Every tool-handling stage
        |
        v
Return a string
```

For example:

```text
Argument error: Missing required argument 'event_name'.
```

Instead of:

```python
raise Exception(...)
```

the system converts many failures into strings.

This allows the model to see what happened.

The model can potentially respond to:

```text
Tool result:
Argument error: Missing required argument 'event_name'.
```

and attempt another call.

This makes the system more robust.

---

# 21. Difference Between `length` and Tool-Argument Errors

These failures are different.

## `length`

This is a generation-budget problem.

The model response was truncated because it reached the token limit.

Repair:

```text
Increase max_tokens
+
Retry
```

---

## Invalid Tool Arguments

This is a data/validation problem.

Example:

```json
{
    "event_name": 123
}
```

Repair:

```text
Return validation error
+
Allow model/application to recover
```

Therefore, these two failure types should not be handled in exactly the same way.

---

# 22. Fault Injection

Fault injection is performed using:

```text
inject_faults.py
```

No model is used.

No internet is required for the fault-injection logic.

The program manually creates fake tool calls.

Example:

```python
FakeCall(
    "get_event_info",
    '{"event_name": "AI_HACKATHON"'
)
```

This deliberately creates malformed JSON.

The handler is then tested directly.

This approach is useful because it isolates the application layer from model randomness.

---

# 23. Fault Injection Table

The following table should be completed using the actual terminal output.

| # | Fault | Expected Result | Run Continued? |
|---:|---|---|---|
| 1 | Good call | Tool executes | Fill after run |
| 2 | Invalid JSON | Error string | Fill after run |
| 3 | Unknown tool | Error string | Fill after run |
| 4 | Missing argument | Validation error | Fill after run |
| 5 | Wrong type | Validation error | Fill after run |
| 6 | Invalid enum | Validation error | Fill after run |
| 7 | Extra argument | Validation error | Fill after run |
| 8 | Unknown event | Tool-level error | Fill after run |
| 9 | Unsafe calculator expression | Calculator error | Fill after run |
| 10 | Empty arguments | Error handling | Fill after run |

Do not invent the final observation.

It should be based on the actual terminal execution.

---

# 24. Schema-Preventable Failure

An example of a schema-preventable failure is:

```json
{
    "event_name": 101
}
```

The schema says:

```text
event_name -> string
```

Therefore the wrong type can be rejected.

Another example is:

```json
{
    "event_name": "AI_HACKATHON",
    "detail": "price"
}
```

The schema defines an enum:

```text
fee
day
venue
category
```

Therefore:

```text
price
```

is invalid.

Another example:

```json
{
    "event_name": "AI_HACKATHON",
    "year": 2026
}
```

can be rejected because:

```text
additionalProperties = false
```

---

# 25. Schema-Not-Preventable Failure

Schema validation cannot guarantee the truth of every value.

For example, suppose the model produces:

```json
{
    "event_name": "AI_HACKATHON"
}
```

This satisfies the schema.

However, the tool implementation could theoretically contain:

```text
fee = 999
```

instead of:

```text
fee = 300
```

The JSON structure is valid.

The semantic data is wrong.

Therefore:

> Schema validation guarantees structure, not truth.

Application logic, databases, business rules, and testing are still required.

---

# 26. Before and After Guards

A major purpose of this project is to compare an unsafe approach with the guarded approach.

## Before Guards

An unguarded system could effectively do:

```text
Model
 ↓
Take arguments
 ↓
Execute function
```

Problems:

- Invalid JSON can crash the parser.
- Unknown tools can cause lookup errors.
- Missing arguments can raise exceptions.
- Wrong types can reach business logic.
- Extra arguments can be accepted accidentally.
- Infinite loops can occur.
- Repeated calls can waste API calls.

---

## After Guards

The project uses:

```text
Model
 ↓
Parse
 ↓
Look up tool
 ↓
Validate
 ↓
Execute
 ↓
Return result
```

Additional protections:

```text
Maximum steps
Repeated-call detection
Length retry
Safe calculator
String-based error handling
```

This is much safer.

---

# 27. Normal Agent Observation

The four main observation questions are:

## Question 1 – Single Tool

```text
What is the fee for the AI Hackathon?
```

Expected behavior:

```text
Model
 ↓
get_event_info
 ↓
AI_HACKATHON + fee
 ↓
300
 ↓
Final answer
```

---

## Question 2 – Two Tools at Once

```text
What are the fee and venue for the AI Hackathon?
```

Expected possible behavior:

```text
Tool call 1 -> fee
Tool call 2 -> venue
```

The exact model behavior should be recorded from the actual run.

If the model makes two calls in parallel, record that.

If it makes one call first and another later, record the actual behavior instead.

---

## Question 3 – Invalid Value Temptation

Example:

```text
What is the fee for the Robotics Competition?
```

The known event is:

```text
ROBOTICS_WORKSHOP
```

not:

```text
ROBOTICS_COMPETITION
```

The model may recognize that the requested event is not present.

If it generates an invalid enum value, the schema/validation layer should reject it.

If it does not generate an invalid value, this should be reported honestly.

The invalid-value behavior is still demonstrated through fault injection.

---

## Question 4 – No Tool

Example:

```text
Write a one-line welcome message for a new student.
```

This question does not require event data or arithmetic.

Therefore the expected behavior is:

```text
No tool call
      ↓
Direct model response
```

---

# 28. Observation Table

The final report should include actual results.

| Question | Tool Needed? | Tool Calls Observed | Result |
|---|---|---|---|
| AI Hackathon fee | Yes | Fill actual result | Fill |
| AI Hackathon fee + venue | Yes | Fill actual result | Fill |
| Robotics Competition fee | Possibly | Fill actual result | Fill |
| Welcome message | No | Fill actual result | Fill |

The important point is that the report should describe what the actual model did, not what we expected it to do.

---

# 29. Structured Output Observation

The structured demo asks the same extraction question in three ways.

Question:

```text
I want to join the AI Hackathon on Saturday
with a student pass and bring 2 guests.
```

The required information is:

```text
event_name
day
pass_type
guest_count
```

---

## No Constraint

The output may be normal natural language.

Example:

```text
The student wants to join the AI Hackathon on Saturday
with a student pass and 2 guests.
```

This is understandable to a human but requires additional parsing if another program needs the data.

---

## JSON Mode

The output is expected to be JSON.

Example:

```json
{
    "event_name": "AI_HACKATHON",
    "day": "Saturday",
    "pass_type": "student",
    "guest_count": 2
}
```

This is easier for programs to consume.

---

## JSON Schema Mode

The response follows the defined schema more strictly.

The expected structure is:

```json
{
    "event_name": "AI_HACKATHON",
    "day": "Saturday",
    "pass_type": "student",
    "guest_count": 2
}
```

The schema also prevents unexpected fields.

---

# 30. Structured Output Comparison Table

| Mode | Human Readability | Machine Readability | Structure Guarantee |
|---|---|---|---|
| No constraint | High | Low | Low |
| JSON mode | Medium | High | Medium |
| JSON Schema mode | Medium | Very high | High |

The exact model output should be captured in the screenshot and discussed based on the actual run.

---

# 31. Important Distinction: Schema vs Truth

An important lesson from the project is:

```text
Schema correctness
≠
Business correctness
```

For example:

```json
{
    "event_name": "AI_HACKATHON",
    "fee": 999
}
```

may have a perfectly valid JSON structure.

But if the real fee is:

```text
₹300
```

then the value is incorrect.

Therefore a reliable system needs both:

```text
Schema validation
+
Trusted application/tool data
```

---

# 32. Why Fault Injection Is Important

Testing only successful cases is not enough.

An AI system must also be tested against:

```text
bad input
unexpected output
invalid arguments
unknown tools
missing data
repeated calls
truncated responses
```

Fault injection makes these failures reproducible.

Instead of waiting for a model to randomly produce a malformed tool call, the test directly constructs one.

This provides a systematic way to test the application's defenses.

---

# 33. Agent Reliability Improvements

The project improves reliability using multiple guards.

## Guard 1 – JSON Parsing

```python
json.loads()
```

is wrapped in error handling.

---

## Guard 2 – Tool Lookup

```python
TOOL_FUNCTIONS.get(name)
```

checks whether the requested tool exists.

---

## Guard 3 – Schema Validation

The validator checks:

```text
required
type
enum
additionalProperties
```

---

## Guard 4 – Tool Execution

The actual Python function is protected by exception handling.

---

## Guard 5 – Length Retry

If:

```text
finish_reason = length
```

the token limit is increased.

---

## Guard 6 – Repeated Calls

Repeated identical calls are detected.

---

## Guard 7 – Maximum Steps

The agent stops after a configured maximum number of iterations.

---

# 34. Why `additionalProperties: false` Matters

Without:

```json
"additionalProperties": false
```

a model could generate:

```json
{
    "event_name": "AI_HACKATHON",
    "fee": 999999,
    "password": "something"
}
```

The application might accidentally accept unwanted fields.

With:

```json
"additionalProperties": false
```

only explicitly defined fields are allowed.

This makes the input contract clearer and safer.

---

# 35. Shared `SCHEMAS` Dictionary

A major implementation requirement is that the project has one shared schema definition.

In:

```text
tools_v2.py
```

the tool definitions are converted into:

```python
SCHEMAS = {
    tool["function"]["name"]:
        tool["function"]["parameters"]
    for tool in TOOLS
}
```

This dictionary is then imported by:

```text
validate.py
```

and:

```text
robust_agent.py
```

This avoids duplication.

Without this approach, it would be possible to accidentally have:

```text
Model schema:
event_name required

Validator schema:
event_name optional
```

which would create inconsistent behavior.

---

# 36. Why the Validator Is Necessary Even With Schema

It may seem unnecessary to validate arguments locally because the model receives a schema.

However, application-level validation is still valuable.

Reasons include:

1. Model behavior can vary.
2. Different providers can have different behaviors.
3. Tool calls may come from other components.
4. Developers may call the tool handler directly.
5. Fault injection requires local validation.
6. Business rules may be stricter than JSON Schema.
7. Valid JSON can still contain semantically incorrect values.

Therefore:

```text
Provider schema constraints
+
Application validation
```

provide defense in depth.

---

# 37. Suitability of Tool Calling

Tool calling is suitable for this project because the assistant needs to perform actual operations.

For example:

```text
Get the AI Hackathon fee.
```

requires retrieving data from:

```text
EVENTS
```

Another example:

```text
Calculate the cost of two registrations.
```

requires executing:

```text
calculate_cost
```

Therefore tool calling is a natural fit.

---

# 38. Suitability of Structured Outputs

Structured outputs are suitable when the application needs data rather than an action.

For example:

```text
Extract:
event name
day
pass type
guest count
```

The application does not need the model to execute a Python function.

It only needs reliable structured information.

Therefore:

```text
Tool calling
→ action

Structured output
→ structured data
```

is a useful mental model.

---

# 39. Generalization to Other Applications

The same architecture can be applied to many real-world systems.

Examples:

## College Assistant

Tools:

```text
get_course_info
get_exam_schedule
get_attendance
```

---

## Banking Assistant

Tools:

```text
get_balance
get_transactions
calculate_interest
```

---

## Shopping Assistant

Tools:

```text
search_product
check_stock
calculate_total
```

---

## Hospital Assistant

Tools:

```text
check_appointment
find_doctor
check_available_slots
```

---

## Travel Assistant

Tools:

```text
search_flights
check_hotel
calculate_trip_cost
```

The architecture remains:

```text
User
 ↓
LLM
 ↓
Tool selection
 ↓
Validation
 ↓
Tool execution
 ↓
Observation
 ↓
LLM
 ↓
Final answer
```

---

# 40. Limitations

The current implementation is educational rather than production-ready.

Some limitations include:

- Local in-memory event data
- No authentication
- No database
- No actual event registration
- No payment system
- No persistent user history
- No distributed execution
- No human approval workflow
- No production monitoring
- Limited calculator operations

These can be added in future versions.

---

# 41. Future Improvements

Possible future improvements include:

### 1. Database

Replace the Python dictionary with:

```text
SQLite
PostgreSQL
MongoDB
```

---

### 2. Real Registration

Add a tool such as:

```text
register_student
```

---

### 3. Availability

Add:

```text
check_event_capacity
```

---

### 4. Authentication

Verify student identity before performing sensitive operations.

---

### 5. Payment

Integrate a payment provider.

---

### 6. Logging

Store:

```text
user question
tool selected
arguments
tool result
final response
```

for debugging.

Sensitive information should not be logged unnecessarily.

---

### 7. Human Approval

For important actions:

```text
Model
 ↓
Tool request
 ↓
Human approval
 ↓
Tool execution
```

This can improve safety.

---

# 42. Overall Conclusion

This project demonstrates that an Agentic AI system is more than a language model.

A reliable agent requires an orchestration layer.

The model provides:

```text
language understanding
+
decision making
+
tool selection
```

The application provides:

```text
validation
+
execution
+
security
+
error handling
+
loop control
```

The complete architecture is:

```text
                 USER
                   |
                   v
             +-----------+
             |    LLM    |
             +-----------+
                   |
             Tool request?
              /         \
            No           Yes
            |             |
            |             v
            |       Parse JSON
            |             |
            |             v
            |        Find Tool
            |             |
            |             v
            |        Validate
            |             |
            |             v
            |         Execute
            |             |
            |             v
            |       Tool Result
            |             |
            |             v
            |<------------+
            |
            v
       Final Answer
```

The most important lessons are:

1. **Model output is untrusted input.**
2. **Tool schemas constrain the expected structure.**
3. **Application validation provides an additional safety layer.**
4. **Every tool call must receive a corresponding tool result.**
5. **Parallel tool calls must all be handled.**
6. **`length` requires a token-budget retry.**
7. **Repeated calls and infinite loops must be controlled.**
8. **Fault injection is useful for testing failure paths.**
9. **JSON mode provides valid JSON, while JSON Schema provides a stronger structural contract.**
10. **Schema correctness does not guarantee factual correctness.**
11. **Tool calling is for actions; structured outputs are for structured data.**
12. **Agent reliability depends on both the model and the surrounding application code.**

The final design can therefore be summarized as:

```text
Agent = Model
      + Tools
      + Schema
      + Validation
      + Execution
      + Observation
      + Loop
      + Error Handling
```

This architecture forms a foundation for building more advanced Agentic AI systems with multiple tools, databases, APIs, memory, human approval, and real-world workflows.