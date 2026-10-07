"""Day 6: check tool arguments against the JSON Schema before calling the function."""

# JSON Schema type mapping
TYPES = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "array": list,
    "object": dict
}


def check_type(value, expected_type):
    """
    Check Python value against expected JSON Schema type.

    Returns True when the type is correct.
    """

    # bool is technically a subclass of int in Python.
    # Therefore, handle boolean separately.
    if expected_type == int:
        return isinstance(value, int) and not isinstance(value, bool)

    if expected_type == (int, float):
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
        )

    return isinstance(value, expected_type)


def validate_arguments(arguments, schema):
    """
    Return None when arguments are valid.

    Otherwise return an error message.
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
    # 3. Check extra arguments
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
    # 4. Check data types and enum values
    # -----------------------------------------------------

    for name, value in arguments.items():

        rule = properties.get(name, {})

        expected_type = TYPES.get(
            rule.get("type")
        )

        if expected_type:

            if not check_type(value, expected_type):

                return (
                    f"Argument '{name}' must be a "
                    f"{rule['type']}, but got "
                    f"{type(value).__name__}: {value!r}."
                )


        # -------------------------------------------------
        # Check enum
        # -------------------------------------------------

        if "enum" in rule:

            if value not in rule["enum"]:

                return (
                    f"Argument '{name}' must be one of "
                    f"{rule['enum']}, got {value!r}."
                )


    # -----------------------------------------------------
    # Everything is valid
    # -----------------------------------------------------

    return None


# ---------------------------------------------------------
# Test validation directly
# ---------------------------------------------------------

if __name__ == "__main__":

    from tools_v2 import SCHEMAS

    schema = SCHEMAS["get_course_fee"]

    cases = [

        {"course_code": "CS101"},

        {"course_code": "CS101", "semester": "even"},

        {},

        {"course_code": 101},

        {"course_code": "CS101", "semester": "summer"},

        {"course_code": "CS101", "year": 2026},
    ]

    print("=" * 80)
    print("VALIDATION TESTS")
    print("=" * 80)

    for case in cases:

        result = validate_arguments(
            case,
            schema
        )

        print(
            f"{str(case):<50} -> "
            f"{result or 'OK'}"
        )

    print("=" * 80)