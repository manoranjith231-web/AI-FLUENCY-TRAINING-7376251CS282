"""
Tools available to the AI Agent.

The agent accesses private student data
through controlled tools.
"""

import json
import os


# student_data.json is in the same folder as tools.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "student_data.json")


def load_data():
    """Load private student data."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_student_info():
    """
    Tool 1:
    Return basic student information.
    """

    data = load_data()

    return data["student"]


def get_subject_info(subject):
    """
    Tool 2:
    Return information about one subject.
    """

    data = load_data()

    subjects = data["subjects"]

    for subject_name, details in subjects.items():

        if subject_name.lower() == subject.lower():

            return {
                "subject": subject_name,
                "marks": details["marks"],
                "attendance": details["attendance"],
                "assignment": details["assignment"]
            }

    return {
        "error": f"Subject '{subject}' was not found."
    }


def get_pending_assignments():
    """
    Tool 3:
    Find subjects whose assignments are pending.
    """

    data = load_data()

    result = []

    for subject, details in data["subjects"].items():

        if details["assignment"].lower() == "pending":

            result.append(subject)

    return result


def get_low_attendance(threshold=80):
    """
    Tool 4:
    Find subjects below attendance threshold.
    """

    data = load_data()

    result = []

    for subject, details in data["subjects"].items():

        if details["attendance"] < threshold:

            result.append({
                "subject": subject,
                "attendance": details["attendance"]
            })

    return result


def get_all_subjects():
    """
    Tool 5:
    Return all subject information.
    """

    data = load_data()

    return data["subjects"]


TOOLS = {
    "get_student_info": get_student_info,
    "get_subject_info": get_subject_info,
    "get_pending_assignments": get_pending_assignments,
    "get_low_attendance": get_low_attendance,
    "get_all_subjects": get_all_subjects
}