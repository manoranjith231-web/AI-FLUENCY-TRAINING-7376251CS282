COURSE_FEES = {
    "CS101": 75000,
    "AI202": 85000,
    "DS303": 80000
}


def get_course_fee(course_code):

    course_code = course_code.upper().strip()

    if course_code in COURSE_FEES:
        return f"The fee for {course_code} is ₹{COURSE_FEES[course_code]:,}."

    return f"No fee information available for {course_code}."