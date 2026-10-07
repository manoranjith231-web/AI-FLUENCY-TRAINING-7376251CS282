"""
Day 6: Fault Injection

No model is used here.
No API call is made.

We manually create broken tool calls
and send them directly to handle_tool_call().
"""

import json

from robust_agent import handle_tool_call


# ---------------------------------------------------------
# Fake function-call objects
# ---------------------------------------------------------

class FakeFunction:

    def __init__(
        self,
        name,
        arguments
    ):

        self.name = name
        self.arguments = arguments


class FakeCall:

    def __init__(
        self,
        name,
        arguments,
        call_id="fault_test"
    ):

        self.id = call_id

        self.type = "function"

        self.function = FakeFunction(
            name,
            arguments
        )


# ---------------------------------------------------------
# Fault cases
# ---------------------------------------------------------

FAULTS = [

    # 1. Good call
    (
        "good call",

        FakeCall(
            "get_event_info",

            json.dumps({
                "event_name": "AI_HACKATHON"
            })
        )
    ),


    # 2. Invalid JSON
    (
        "invalid JSON",

        FakeCall(
            "get_event_info",

            '{"event_name": "AI_HACKATHON"'
        )
    ),


    # 3. Unknown tool
    (
        "unknown tool",

        FakeCall(
            "send_email",

            json.dumps({
                "to": "student@college.edu"
            })
        )
    ),


    # 4. Missing required argument
    (
        "missing required argument",

        FakeCall(
            "get_event_info",

            "{}"
        )
    ),


    # 5. Wrong type
    (
        "wrong type",

        FakeCall(
            "get_event_info",

            json.dumps({
                "event_name": 101
            })
        )
    ),


    # 6. Invalid enum
    (
        "value outside enum",

        FakeCall(
            "get_event_info",

            json.dumps({
                "event_name": "AI_HACKATHON",
                "detail": "price"
            })
        )
    ),


    # 7. Invented argument
    (
        "invented extra argument",

        FakeCall(
            "get_event_info",

            json.dumps({
                "event_name": "AI_HACKATHON",
                "year": 2026
            })
        )
    ),


    # 8. Unknown event
    (
        "unknown event",

        FakeCall(
            "get_event_info",

            json.dumps({
                "event_name": "SPORTS_DAY"
            })
        )
    ),


    # 9. Unsafe calculator
    (
        "unsafe calculator expression",

        FakeCall(
            "calculate_cost",

            json.dumps({
                "expression":
                    "__import__('os').system('dir')"
            })
        )
    ),


    # 10. Empty arguments
    (
        "empty arguments",

        FakeCall(
            "calculate_cost",

            ""
        )
    ),

]


# ---------------------------------------------------------
# Run fault injection
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 100)

    print(
        "DAY 6 - FAULT INJECTION"
    )

    print(
        "No model and no internet are used."
    )

    print("=" * 100)


    for label, call in FAULTS:

        result = handle_tool_call(
            call,
            log=False
        )

        print(
            f"\n{label:<30} -> "
            f"{result}"
        )


    print("\n" + "=" * 100)

    print(
        "Every fault was handled as a STRING."
    )

    print(
        "The handler did not crash."
    )

    print("=" * 100)