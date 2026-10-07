"""
Day 6: Structured Output Demonstration.

The same extraction question is asked three ways:

1. No constraint
2. JSON mode
3. JSON Schema mode
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI


# ---------------------------------------------------------
# Load .env
# ---------------------------------------------------------

load_dotenv()


API_KEY = os.getenv("GROQ_API_KEY")

MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)


# ---------------------------------------------------------
# Client
# ---------------------------------------------------------

client = OpenAI(

    api_key=API_KEY,

    base_url="https://api.groq.com/openai/v1"
)


# ---------------------------------------------------------
# Structured schema
# ---------------------------------------------------------

SCHEMA = {

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

        "day": {
            "type": "string"
        },

        "pass_type": {

            "type": "string",

            "enum": [
                "student",
                "guest"
            ]
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

    "additionalProperties": False
}


# ---------------------------------------------------------
# Same question for all three tests
# ---------------------------------------------------------

QUESTION = (
    "I want to join the AI Hackathon on Saturday "
    "with a student pass and bring 2 guests."
)


# ---------------------------------------------------------
# Ask model
# ---------------------------------------------------------

def ask(
    response_format,
    label,
    system_message
):

    print("\n" + "=" * 80)

    print(label)

    print("=" * 80)


    try:

        response = client.chat.completions.create(

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
            response
            .choices[0]
            .message
            .content
            .strip()
        )


        print("\nRAW REPLY:")
        print(text)


        try:

            parsed = json.loads(text)

            print("\nPARSED RESULT:")
            print(
                json.dumps(
                    parsed,
                    indent=2
                )
            )

        except json.JSONDecodeError as error:

            print(
                "\nJSON PARSE ERROR:"
            )

            print(error)


    except Exception as error:

        print(
            "\nPROVIDER ERROR:"
        )

        print(
            f"{type(error).__name__}: "
            f"{error}"
        )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 80)

    print(
        "DAY 6 - STRUCTURED OUTPUT DEMO"
    )

    print(
        f"MODEL: {MODEL}"
    )

    print("=" * 80)


    # -----------------------------------------------------
    # 1. No constraint
    # -----------------------------------------------------

    ask(

        None,

        "1. NO CONSTRAINT",

        (
            "Extract the event registration details "
            "from the user's sentence. "
            "You may answer normally."
        )
    )


    # -----------------------------------------------------
    # 2. JSON mode
    # -----------------------------------------------------

    ask(

        {
            "type": "json_object"
        },

        "2. JSON MODE",

        (
            "Extract the event registration details. "
            "Return a JSON object only. "
            "Use keys: event_name, day, "
            "pass_type, guest_count."
        )
    )


    # -----------------------------------------------------
    # 3. Strict JSON Schema mode
    # -----------------------------------------------------

    ask(

        {
            "type": "json_schema",

            "json_schema": {

                "name": "event_registration",

                "strict": True,

                "schema": SCHEMA
            }
        },

        "3. JSON SCHEMA MODE",

        (
            "Extract the event registration details "
            "according to the provided schema."
        )
    )