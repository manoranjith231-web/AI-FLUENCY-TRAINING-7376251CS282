"""Day 6: robust Groq agent with validation and retry."""

import json
import os
from dotenv import load_dotenv

load_dotenv()
from groq import Groq

from tools_v2 import TOOLS, TOOL_FUNCTIONS, SCHEMAS
from validate import validate_arguments


# ---------------------------------------------------------
# Groq configuration
# ---------------------------------------------------------

MODEL = "openai/gpt-oss-20b"

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not set. "
        "Set it before running the program."
    )


client = Groq(
    api_key=API_KEY
)


# ---------------------------------------------------------
# System prompt
# ---------------------------------------------------------

SYSTEM_PROMPT = (
    "You are a college fee assistant. "
    "Never guess a fee: always call get_course_fee. "
    "Use calculator for every arithmetic step. "
    "Valid course codes: CS101, AI202, DS303. "
    "If no tool is needed, answer directly."
)


# ---------------------------------------------------------
# Settings
# ---------------------------------------------------------

MAX_TOKENS = 500

REPEAT_LIMIT = 3


# ---------------------------------------------------------
# Handle one tool call
# ---------------------------------------------------------

def handle_tool_call(call, log=True):
    """
    Execute one tool call safely.

    Always returns a string so the model can continue.
    """

    name = call.function.name

    raw = call.function.arguments or "{}"


    # -----------------------------------------------------
    # 1. Validate JSON
    # -----------------------------------------------------

    try:

        arguments = json.loads(raw)

    except json.JSONDecodeError as error:

        return (
            f"Argument error: invalid JSON ({error}). "
            f"Send valid JSON for '{name}'."
        )


    # -----------------------------------------------------
    # 2. Check whether tool exists
    # -----------------------------------------------------

    function = TOOL_FUNCTIONS.get(name)

    if function is None:

        return (
            f"Unknown tool: {name}. "
            f"Available tools: "
            f"{', '.join(TOOL_FUNCTIONS)}."
        )


    # -----------------------------------------------------
    # 3. Validate arguments against schema
    # -----------------------------------------------------

    problem = validate_arguments(
        arguments,
        SCHEMAS[name]
    )

    if problem:

        return f"Argument error: {problem}"


    # -----------------------------------------------------
    # 4. Execute tool safely
    # -----------------------------------------------------

    try:

        result = str(
            function(**arguments)
        )

    except Exception as error:

        result = (
            f"Tool error in {name}: "
            f"{type(error).__name__}: {error}"
        )


    # -----------------------------------------------------
    # 5. Print tool execution
    # -----------------------------------------------------

    if log:

        print(
            f"      {name}({arguments}) "
            f"-> {result[:100]}"
        )


    return result


# ---------------------------------------------------------
# Agent
# ---------------------------------------------------------

def agent(
    question,
    max_steps=6,
    verbose=True
):
    """
    Run the Groq agent.

    The agent can repeatedly:
        model -> tool -> result -> model
    until it gives a final answer.
    """

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


    seen = {}

    max_tokens = MAX_TOKENS


    # -----------------------------------------------------
    # Agent loop
    # -----------------------------------------------------

    for step in range(1, max_steps + 1):

        try:

            response = client.chat.completions.create(

                model=MODEL,

                messages=messages,

                tools=TOOLS,

                temperature=0,

                max_completion_tokens=max_tokens
            )

        except Exception as error:

            return (
                f"Groq API error: "
                f"{type(error).__name__}: {error}"
            )


        choice = response.choices[0]

        message = choice.message


        # -------------------------------------------------
        # Handle truncated response
        # -------------------------------------------------

        if choice.finish_reason == "length":

            if max_tokens >= 2000:

                return (
                    "Stopped: the reply was still "
                    "truncated at 2000 tokens."
                )


            max_tokens *= 2


            if verbose:

                print(
                    f"   step {step}: truncated, "
                    f"retrying with max_tokens={max_tokens}"
                )


            continue


        # -------------------------------------------------
        # No tool call = final answer
        # -------------------------------------------------

        if not message.tool_calls:

            return (
                message.content or ""
            ).strip()


        # -------------------------------------------------
        # Add assistant tool-call message
        # -------------------------------------------------

        messages.append({

            "role": "assistant",

            "content": message.content or "",

            "tool_calls": [

                {
                    "id": call.id,

                    "type": "function",

                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments
                    }
                }

                for call in message.tool_calls
            ]
        })


        if verbose:

            print(
                f"   step {step}: "
                f"{len(message.tool_calls)} tool call(s)"
            )


        # -------------------------------------------------
        # Execute every tool call
        # -------------------------------------------------

        for call in message.tool_calls:

            signature = (
                call.function.name,
                call.function.arguments
            )


            seen[signature] = (
                seen.get(signature, 0) + 1
            )


            # ---------------------------------------------
            # Prevent infinite repeated calls
            # ---------------------------------------------

            if seen[signature] >= REPEAT_LIMIT:

                return (
                    f"Stopped: {call.function.name} "
                    f"was called {REPEAT_LIMIT} times "
                    f"with the same arguments and "
                    f"made no progress."
                )


            # ---------------------------------------------
            # Execute tool
            # ---------------------------------------------

            result = handle_tool_call(
                call,
                log=verbose
            )


            # ---------------------------------------------
            # Send result back to Groq
            # ---------------------------------------------

            messages.append({

                "role": "tool",

                "tool_call_id": call.id,

                "name": call.function.name,

                "content": result
            })


    # -----------------------------------------------------
    # Maximum steps reached
    # -----------------------------------------------------

    return (
        "Stopped: maximum steps reached "
        "without a final answer."
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 78)
    print("ROBUST GROQ AGENT")
    print("=" * 78)

    print(f"Model: {MODEL}")


    questions = [

        "What is the total fee for CS101 and AI202 after a 10% scholarship?",

        "Is DS303 more expensive than CS101, and by how much?",

        "What is the fee for ME404?",

        "Write a one-line welcome message for new students."
    ]


    for question in questions:

        print("\nQ:", question)

        answer = agent(question)

        print("A:", answer)


    print("=" * 78)