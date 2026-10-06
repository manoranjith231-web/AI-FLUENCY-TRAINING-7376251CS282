"""
Rule-Based Workflow
-------------------

Architecture:

User
  |
  v
Predefined Rules
  |
  v
Private JSON Data
  |
  v
Response
"""

import json
import os


# student_data.json is in the same folder as workflow.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "student_data.json")


def load_data():
    """Load private student data from JSON."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def workflow(question, data):

    question = question.lower()
    subjects = data["subjects"]

    # Rule 1: DBMS marks
    if "dbms" in question and "mark" in question:

        marks = subjects["DBMS"]["marks"]

        return f"DBMS marks: {marks}/100"

    # Rule 2: Pending assignments
    elif "pending" in question and "assignment" in question:

        pending = []

        for subject, details in subjects.items():

            if details["assignment"].lower() == "pending":
                pending.append(subject)

        if pending:
            return (
                "Subjects with pending assignments:\n"
                + "\n".join(f"- {subject}" for subject in pending)
            )

        return "There are no pending assignments."

    # Rule 3: Attendance below 80
    elif "attendance" in question and (
        "below" in question
        or "less" in question
        or "under" in question
    ):

        result = []

        for subject, details in subjects.items():

            if details["attendance"] < 80:

                result.append(
                    f"- {subject}: {details['attendance']}%"
                )

        if result:
            return (
                "Subjects with attendance below 80%:\n"
                + "\n".join(result)
            )

        return "No subject has attendance below 80%."

    # Rule 4: General attendance
    elif "attendance" in question:

        result = []

        for subject, details in subjects.items():

            result.append(
                f"- {subject}: {details['attendance']}%"
            )

        return "Attendance:\n" + "\n".join(result)

    # Rule 5: Student information
    elif "student" in question or "my details" in question:

        student = data["student"]

        return (
            f"Name: {student['name']}\n"
            f"Department: {student['department']}\n"
            f"Year: {student['year']}\n"
            f"Semester: {student['semester']}"
        )

    # Rule 6: All subjects
    elif "all subjects" in question:

        result = []

        for subject, details in subjects.items():

            result.append(
                f"- {subject}: "
                f"{details['marks']} marks, "
                f"{details['attendance']}% attendance, "
                f"{details['assignment']}"
            )

        return "Subjects:\n" + "\n".join(result)

    else:

        return (
            "No predefined rule matches this question.\n"
            "The workflow can only handle questions that "
            "have been programmed into its rules."
        )


def main():

    data = load_data()

    print("=" * 55)
    print("          RULE-BASED WORKFLOW")
    print("=" * 55)

    print("\nPrivate student data is available.")
    print("No LLM is used.")
    print("Type 'exit' to stop.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":

            print("Workflow: Goodbye!")
            break

        answer = workflow(question, data)

        print("\nWorkflow:")
        print(answer)
        print()


if __name__ == "__main__":
    main()