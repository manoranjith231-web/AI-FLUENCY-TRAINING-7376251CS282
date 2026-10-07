"""Day 6: force the Groq model to answer in a fixed JSON shape."""

import json
import os
from dotenv import load_dotenv

load_dotenv()
from groq import Groq


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
# JSON Schema
# ---------------------------------------------------------

SCHEMA = {

    "type": "object",

    "properties": {

        "course_code": {
            "type": "string"
        },

        "wants_scholarship": {
            "type": "boolean"
        },

        "needs_tool": {
            "type": "boolean"
        }
    },

    "required": [
        "course_code",
        "wants_scholarship",
        "needs_tool"
    ],

    "additionalProperties": False
}


# ---------------------------------------------------------
# Question
# ---------------------------------------------------------

QUESTION = (
    "What do I pay for AI202 "
    "if I have the merit scholarship?"
)


# ---------------------------------------------------------
# Ask Groq
# ---------------------------------------------------------

def ask(
    response_format,
    label,
    system_message=(
        "Extract the request details as JSON. "
        "Reply with JSON only."
    )
):

    print(f"\n--- {label} ---")


    try:

        reply = client.chat.completions.create(

            model=MODEL,

            messages=[

                {
                    "role": "system",
                    "content": system_message
                },

                {
                    "role": "user",
                    "content": QUESTION
                }
            ],

            temperature=0,

            response_format=response_format
        )


        text = (
            reply
            .choices[0]
            .message
            .content
            .strip()
        )


        print("raw    :", text)


        parsed = json.loads(text)


        print(
            "parsed :",
            json.dumps(
                parsed,
                indent=2
            )
        )


    except Exception as error:

        print(
            f"not supported / failed "
            f"({type(error).__name__}: {error})"
        )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 78)
    print("GROQ STRUCTURED OUTPUTS")
    print("=" * 78)


    # -----------------------------------------------------
    # 1. No response constraint
    # -----------------------------------------------------

    ask(
        None,
        "1. no constraint (free text)",
        system_message=(
            "Answer the user's question normally."
        )
    )


    # -----------------------------------------------------
    # 2. JSON mode
    # -----------------------------------------------------

    ask(
        {
            "type": "json_object"
        },

        "2. JSON mode: valid JSON, any shape",

        system_message=(
            "Extract the request details. "
            "Return valid JSON only."
        )
    )


    # -----------------------------------------------------
    # 3. Strict JSON Schema
    # -----------------------------------------------------

    ask(

        {
            "type": "json_schema",

            "json_schema": {

                "name": "fee_query",

                "strict": True,

                "schema": SCHEMA
            }
        },

        "3. schema mode: valid JSON in YOUR shape",

        system_message=(
            "Extract the request details using "
            "the exact required schema."
        )
    )


    print("\n" + "=" * 78)