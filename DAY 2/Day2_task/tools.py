# tools.py

COURSE_FEES = {
    "CS101": 45000,
    "AI202": 55000,
    "DS303": 50000
}


def get_course_fee(course_code):
    """
    Tool used to retrieve the fee of a course.
    """

    course_code = course_code.upper()

    if course_code in COURSE_FEES:
        return {
            "course_code": course_code,
            "fee": COURSE_FEES[course_code]
        }

    return {
        "error": "Course not found"
    }


def calculator(expression):
    """
    Simple calculator tool.
    """

    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return result

    except Exception:
        return "Invalid mathematical expression"


def list_courses():
    """
    Returns all available courses and fees.
    """

    return COURSE_FEES