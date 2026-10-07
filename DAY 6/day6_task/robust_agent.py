"""
Day 6: Robust Campus Event Agent.

Uses:
- Groq API
- OpenAI-compatible Chat Completions
- Tool calling
- JSON Schema validation
- Retry
- Parallel tool calls
- Loop protection
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools_v2 import (
    TOOLS,
    TOOL_FUNCTIONS,
    SCHEMAS,
)

from validate import validate_arguments


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv()


API_KEY = os.getenv("GROQ_API_KEY")

MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)


# ---------------------------------------------------------
# Create OpenAI-compatible Groq client
# ---------------------------------------------------------

def create_client():

    if not API_KEY:

        raise RuntimeError(
            "GROQ_API_KEY is not set. "
            "Add your Groq API key to .env"
        )

    return OpenAI(
        api_key=API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )


# ---------------------------------------------------------
# System prompt
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are a Campus Event Assistant.

You help students with college event information.

Rules:

1. Never guess event fees.
2. Use get_event_info when event information is required.
3. Use calculate_cost for arithmetic.
4. Valid events are:
   AI_HACKATHON
   ROBOTICS_WORKSHOP
   CULTURAL_FEST

5. If two independent event lookups are required,
   call the tools in parallel when possible.
6. If no tool is required, answer directly.
7. If a tool returns an error, use that information
   and try to recover instead of crashing.
"""


# ---------------------------------------------------------
# Tool handler
# ---------------------------------------------------------

def handle_tool_call(call, log=True):
    """
    Safely handle ONE model-generated tool call.

    Four stages:

    1. Parse JSON
    2. Look up tool
    3. Validate arguments
    4. Execute tool

    Every failure becomes a string.
    """

    name = call.function.name

    raw = call.function.arguments or "{}"


    # -----------------------------------------------------
    # Stage 1: Parse JSON
    # -----------------------------------------------------

    try:

        arguments = json.loads(raw)

    except json.JSONDecodeError as error:

        return (
            f"Argument error: invalid JSON "
            f"({error}). "
            f"Send valid JSON for '{name}'."
        )


    # -----------------------------------------------------
    # Stage 2: Look up tool
    # -----------------------------------------------------

    function = TOOL_FUNCTIONS.get(name)

    if function is None:

        return (
            f"Unknown tool: {name}. "
            f"Available tools: "
            f"{', '.join(TOOL_FUNCTIONS)}."
        )


    # -----------------------------------------------------
    # Stage 3: Validate arguments
    # -----------------------------------------------------

    problem = validate_arguments(
        arguments,
        SCHEMAS[name]
    )

    if problem:

        return f"Argument error: {problem}"


    # -----------------------------------------------------
    # Stage 4: Execute tool
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


    if log:

        print(
            f"      {name}({arguments}) -> "
            f"{result[:120]}"
        )


    return result


# ---------------------------------------------------------
# Main agent
# ---------------------------------------------------------

def agent(
    question,
    max_steps=6,
    verbose=True
):

    client = create_client()


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

    max_tokens = 500


    # -----------------------------------------------------
    # Agent loop
    # -----------------------------------------------------

    for step in range(
        1,
        max_steps + 1
    ):

        if verbose:

            print(
                f"\n   STEP {step}"
            )


        try:

            response = client.chat.completions.create(

                model=MODEL,

                messages=messages,

                tools=TOOLS,

                tool_choice="auto",

                parallel_tool_calls=True,

                temperature=0,

                max_tokens=max_tokens,
            )

        except Exception as error:

            return (
                f"API error: "
                f"{type(error).__name__}: {error}"
            )


        choice = response.choices[0]

        message = choice.message

        finish_reason = choice.finish_reason


        if verbose:

            print(
                f"   finish_reason = "
                f"{finish_reason}"
            )


        # -------------------------------------------------
        # Case 1: truncated response
        # -------------------------------------------------

        if finish_reason == "length":

            if max_tokens >= 2000:

                return (
                    "Stopped: reply was still "
                    "truncated at 2000 tokens."
                )

            max_tokens *= 2

            if verbose:

                print(
                    "   Reply was truncated."
                )

                print(
                    f"   Retrying with "
                    f"max_tokens={max_tokens}"
                )

            continue


        # -------------------------------------------------
        # Case 2: final answer
        # -------------------------------------------------

        if not message.tool_calls:

            return (
                message.content or ""
            ).strip()


        # -------------------------------------------------
        # Model requested one or more tools
        # -------------------------------------------------

        if verbose:

            print(
                f"   Tool calls received: "
                f"{len(message.tool_calls)}"
            )


        # -------------------------------------------------
        # Save assistant tool-call message
        # -------------------------------------------------

        messages.append({

            "role": "assistant",

            "content": message.content or "",

            "tool_calls": [

                {
                    "id": call.id,

                    "type": "function",

                    "function": {
                        "name":
                            call.function.name,

                        "arguments":
                            call.function.arguments,
                    }
                }

                for call in message.tool_calls
            ]
        })


        # -------------------------------------------------
        # IMPORTANT:
        # Handle EVERY tool call.
        # -------------------------------------------------

        for call in message.tool_calls:

            signature = (
                call.function.name,
                call.function.arguments
            )


            # ---------------------------------------------
            # Repeated identical call protection
            # ---------------------------------------------

            seen[signature] = (
                seen.get(signature, 0) + 1
            )


            if seen[signature] >= 3:

                return (
                    f"Stopped: "
                    f"{call.function.name} "
                    f"was called 3 times with "
                    f"the same arguments."
                )


            # ---------------------------------------------
            # Execute safely
            # ---------------------------------------------

            result = handle_tool_call(
                call,
                log=verbose
            )


            # ---------------------------------------------
            # Send tool result back
            # ---------------------------------------------

            messages.append({

                "role": "tool",

                "tool_call_id": call.id,

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
# Demonstration
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 80)
    print("DAY 6 - ROBUST CAMPUS EVENT AGENT")
    print("=" * 80)

    questions = [

        # 1. Single tool
        "What is the fee for the AI Hackathon?",

        # 2. Two independent lookups
        (
            "What are the fee and venue for the "
            "AI Hackathon?"
        ),

        # 3. Calculation
        (
            "How much would 2 AI Hackathon registrations "
            "cost?"
        ),

        # 4. Invalid / unknown event
        (
            "What is the fee for the Robotics Competition?"
        ),

        # 5. No tool
        "Write a one-line welcome message for a new student.",
    ]


    for question in questions:

        print("\n" + "-" * 80)

        print("QUESTION:")
        print(question)

        answer = agent(
            question,
            verbose=True
        )

        print("\nFINAL ANSWER:")
        print(answer)

    print("=" * 80)