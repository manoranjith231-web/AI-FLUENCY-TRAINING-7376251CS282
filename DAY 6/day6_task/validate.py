"""
Day 6: JSON Schema argument validator.

The validator checks tool arguments BEFORE
the actual Python function is executed.
"""


TYPES = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "array": list,
    "object": dict,
}


def validate_arguments(arguments, schema):
    """
    Return None when arguments are valid.

    Return an error message when arguments
    are invalid.
    """

    # -----------------------------------------------------
    # 1. Arguments must be a JSON object
    # -----------------------------------------------------

    if not isinstance(arguments, dict):
        return "Arguments must be a JSON object."


    properties = schema.get("properties", {})


    # -----------------------------------------------------
    # 2. Check required arguments
    # -----------------------------------------------------

    for name in schema.get("required", []):

        if name not in arguments:

            return (
                f"Missing required argument '{name}'. "
                f"Expected: {', '.join(properties)}."
            )


    # -----------------------------------------------------
    # 3. Check invented / extra arguments
    # -----------------------------------------------------

    if schema.get("additionalProperties") is False:

        extra = [
            key
            for key in arguments
            if key not in properties
        ]

        if extra:

            return (
                f"Unexpected argument(s): {', '.join(extra)}. "
                f"Allowed: {', '.join(properties)}."
            )


    # -----------------------------------------------------
    # 4. Check type and enum
    # -----------------------------------------------------

    for name, value in arguments.items():

        rule = properties.get(name, {})

        expected = TYPES.get(
            rule.get("type")
        )

        # Type validation
        if expected and not isinstance(value, expected):

            return (
                f"Argument '{name}' must be a "
                f"{rule['type']}, but got "
                f"{type(value).__name__}: {value!r}."
            )


        # Enum validation
        if "enum" in rule:

            if value not in rule["enum"]:

                return (
                    f"Argument '{name}' must be one of "
                    f"{rule['enum']}, got {value!r}."
                )


    return None


# ---------------------------------------------------------
# Manual validator testing
# ---------------------------------------------------------

if __name__ == "__main__":

    from tools_v2 import SCHEMAS

    schema = SCHEMAS["get_event_info"]

    cases = [

        # Good
        {
            "event_name": "AI_HACKATHON"
        },

        # Good with enum
        {
            "event_name": "AI_HACKATHON",
            "detail": "venue"
        },

        # Missing required
        {},

        # Wrong type
        {
            "event_name": 101
        },

        # Invalid enum
        {
            "event_name": "AI_HACKATHON",
            "detail": "price"
        },

        # Invented argument
        {
            "event_name": "AI_HACKATHON",
            "year": 2026
        },

    ]

    print("=" * 80)
    print("VALIDATOR TEST")
    print("=" * 80)

    for case in cases:

        result = validate_arguments(
            case,
            schema
        )

        print(
            f"{str(case):<60} -> "
            f"{result or 'OK'}"
        )

    print("=" * 80)