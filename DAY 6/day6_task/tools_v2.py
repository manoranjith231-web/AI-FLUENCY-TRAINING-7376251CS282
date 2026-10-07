"""
Day 6: Campus Event Assistant
Tools and JSON Schemas.

Scenario:
A college student asks about campus events and registration costs.
"""

import ast
import operator


# ---------------------------------------------------------
# Campus event data
# ---------------------------------------------------------

EVENTS = {
    "AI_HACKATHON": {
        "fee": 300,
        "day": "Saturday",
        "venue": "Innovation Lab",
        "category": "technical",
    },
    "ROBOTICS_WORKSHOP": {
        "fee": 250,
        "day": "Friday",
        "venue": "Robotics Lab",
        "category": "technical",
    },
    "CULTURAL_FEST": {
        "fee": 150,
        "day": "Monday",
        "venue": "Main Auditorium",
        "category": "cultural",
    },
}


# ---------------------------------------------------------
# Tool 1: Get event information
# ---------------------------------------------------------

def get_event_info(event_name: str, detail: str = "fee") -> str:
    """
    Return information about one campus event.
    """

    event_name = event_name.strip().upper()

    event = EVENTS.get(event_name)

    if event is None:
        return (
            f"Unknown event: {event_name}. "
            f"Valid events: {', '.join(EVENTS)}"
        )

    if detail == "fee":
        return str(event["fee"])

    if detail == "day":
        return event["day"]

    if detail == "venue":
        return event["venue"]

    if detail == "category":
        return event["category"]

    return f"Unknown detail: {detail}"


# ---------------------------------------------------------
# Safe calculator
# ---------------------------------------------------------

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def _evaluate(node):
    """
    Safely evaluate basic arithmetic.
    """

    if isinstance(node, ast.Constant) and isinstance(
        node.value, (int, float)
    ):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)

        return _OPS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.operand))

    raise ValueError(
        "Unsupported expression. Use only numbers and + - * / ( )."
    )


def calculate_cost(expression: str) -> str:
    """
    Safely calculate a simple arithmetic expression.
    """

    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree.body)
        return str(result)

    except Exception as error:
        return f"Calculator error: {error}"


# ---------------------------------------------------------
# Python functions available to the agent
# ---------------------------------------------------------

TOOL_FUNCTIONS = {
    "get_event_info": get_event_info,
    "calculate_cost": calculate_cost,
}


# ---------------------------------------------------------
# Tool definitions sent to the model
# ---------------------------------------------------------

TOOLS = [

    {
        "type": "function",
        "function": {
            "name": "get_event_info",
            "description": (
                "Get information about one campus event. "
                "Valid events are AI_HACKATHON, ROBOTICS_WORKSHOP "
                "and CULTURAL_FEST."
            ),
            "parameters": {
                "type": "object",

                "properties": {
                    "event_name": {
                        "type": "string",
                        "enum": [
                            "AI_HACKATHON",
                            "ROBOTICS_WORKSHOP",
                            "CULTURAL_FEST",
                        ],
                        "description": "Campus event name.",
                    },

                    "detail": {
                        "type": "string",
                        "enum": [
                            "fee",
                            "day",
                            "venue",
                            "category",
                        ],
                        "description": "Which event detail is required.",
                    },
                },

                "required": [
                    "event_name"
                ],

                "additionalProperties": False,
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "calculate_cost",
            "description": (
                "Calculate a basic arithmetic expression using "
                "+, -, *, / and brackets."
            ),

            "parameters": {
                "type": "object",

                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "Arithmetic expression such as "
                            "300 * 2 + 150."
                        ),
                    }
                },

                "required": [
                    "expression"
                ],

                "additionalProperties": False,
            },
        },
    },
]


# ---------------------------------------------------------
# One schema dictionary used by BOTH:
# 1. The model
# 2. The validator
# ---------------------------------------------------------

SCHEMAS = {
    tool["function"]["name"]:
        tool["function"]["parameters"]
    for tool in TOOLS
}


if __name__ == "__main__":

    print("=" * 70)
    print("CAMPUS EVENT ASSISTANT - AVAILABLE TOOLS")
    print("=" * 70)

    print("\nEvents:")

    for name, data in EVENTS.items():
        print(
            f"{name}: ₹{data['fee']} | "
            f"{data['day']} | "
            f"{data['venue']}"
        )

    print("\nTools:")

    for tool in TOOLS:
        print(
            "-",
            tool["function"]["name"]
        )

    print("\nSchemas loaded successfully.")