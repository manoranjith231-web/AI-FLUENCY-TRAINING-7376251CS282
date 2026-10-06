"""
AI Agent
--------

Architecture:

User
  |
  v
LLM / Agent Decision
  |
  v
Tool Selection
  |
  v
Tool Execution
  |
  v
Observation
  |
  v
LLM / Agent Decision
  |
  +------> More work? ------+
  |                         |
  |                         |
  +-------------------------+
  |
  v
Final Answer

For demonstration purposes this project supports DEMO_MODE.
"""

import os
import sys

# Allow Python to import tools.py from the same folder
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from tools import (
    get_student_info,
    get_subject_info,
    get_pending_assignments,
    get_low_attendance,
    get_all_subjects
)


# ---------------------------------------------------------
# Tool execution
# ---------------------------------------------------------

def execute_tool(tool_name, arguments=None):
    """
    Execute the tool selected by the agent.
    """

    arguments = arguments or {}

    if tool_name == "get_student_info":

        return get_student_info()

    elif tool_name == "get_subject_info":

        return get_subject_info(
            arguments.get("subject", "")
        )

    elif tool_name == "get_pending_assignments":

        return get_pending_assignments()

    elif tool_name == "get_low_attendance":

        threshold = arguments.get("threshold", 80)

        return get_low_attendance(threshold)

    elif tool_name == "get_all_subjects":

        return get_all_subjects()

    else:

        return {
            "error": f"Unknown tool: {tool_name}"
        }


# ---------------------------------------------------------
# Demo agent decision
# ---------------------------------------------------------

def choose_tool_demo(question):
    """
    Simulated agent decision.

    In a real LLM agent, the LLM would choose the tool.
    This function demonstrates the same tool-selection concept
    without requiring an API key.
    """

    question_lower = question.lower()

    # Pending assignments
    if (
        "pending" in question_lower
        and "assignment" in question_lower
    ):

        return (
            "get_pending_assignments",
            {}
        )

    # Low attendance
    if (
        "attendance" in question_lower
        and (
            "below" in question_lower
            or "less" in question_lower
            or "under" in question_lower
        )
    ):

        return (
            "get_low_attendance",
            {
                "threshold": 80
            }
        )

    # DBMS
    if "dbms" in question_lower:

        return (
            "get_subject_info",
            {
                "subject": "DBMS"
            }
        )

    # Python
    if "python" in question_lower:

        return (
            "get_subject_info",
            {
                "subject": "Python"
            }
        )

    # Data Structures
    if (
        "data structures" in question_lower
        or "datastructures" in question_lower
    ):

        return (
            "get_subject_info",
            {
                "subject": "Data Structures"
            }
        )

    # Operating Systems
    if (
        "operating systems" in question_lower
        or "os" in question_lower
    ):

        return (
            "get_subject_info",
            {
                "subject": "Operating Systems"
            }
        )

    # Student information
    if (
        "student" in question_lower
        or "my details" in question_lower
        or "my information" in question_lower
    ):

        return (
            "get_student_info",
            {}
        )

    # All subjects
    if (
        "all subjects" in question_lower
        or "subjects" in question_lower
    ):

        return (
            "get_all_subjects",
            {}
        )

    return None, {}


# ---------------------------------------------------------
# Convert tool result to human-readable answer
# ---------------------------------------------------------

def generate_answer(question, tool_name, result):

    if tool_name == "get_pending_assignments":

        if not result:

            return "There are no pending assignments."

        return (
            "The subjects with pending assignments are: "
            + ", ".join(result)
            + "."
        )

    if tool_name == "get_low_attendance":

        if not result:

            return "No subjects have attendance below 80%."

        lines = []

        for item in result:

            lines.append(
                f"{item['subject']} ({item['attendance']}%)"
            )

        return (
            "The subjects with attendance below 80% are: "
            + ", ".join(lines)
            + "."
        )

    if tool_name == "get_subject_info":

        if "error" in result:

            return result["error"]

        return (
            f"{result['subject']}: "
            f"marks = {result['marks']}/100, "
            f"attendance = {result['attendance']}%, "
            f"assignment = {result['assignment']}."
        )

    if tool_name == "get_student_info":

        return (
            f"Student: {result['name']}\n"
            f"Department: {result['department']}\n"
            f"Year: {result['year']}\n"
            f"Semester: {result['semester']}"
        )

    if tool_name == "get_all_subjects":

        lines = []

        for subject, details in result.items():

            lines.append(
                f"{subject}: "
                f"{details['marks']} marks, "
                f"{details['attendance']}% attendance, "
                f"{details['assignment']}"
            )

        return "\n".join(lines)

    return str(result)


# ---------------------------------------------------------
# Agent loop
# ---------------------------------------------------------

def run_demo_agent(question):

    print("\nUSER")
    print("----")
    print(question)

    print("\nAGENT")
    print("-----")
    print("Reasoning about the request...")

    # Agent decides what to do
    tool_name, arguments = choose_tool_demo(question)

    if tool_name is None:

        print(
            "No suitable tool was found for this request."
        )

        print(
            "\nFINAL ANSWER"
        )

        print(
            "I could not find a suitable tool to answer "
            "this question."
        )

        return

    # Tool selection
    print(
        f"Selected tool: {tool_name}"
    )

    if arguments:

        print(
            f"Tool arguments: {arguments}"
        )

    # Execute selected tool
    print("\nTOOL CALL")
    print("---------")

    result = execute_tool(
        tool_name,
        arguments
    )

    print(
        f"{tool_name}()"
    )

    # Observation
    print("\nOBSERVATION")
    print("-----------")

    print(result)

    # Agent checks result
    print("\nAGENT")
    print("-----")

    print(
        "Tool result received. "
        "Processing the observation..."
    )

    # Final response
    answer = generate_answer(
        question,
        tool_name,
        result
    )

    print("\nFINAL ANSWER")
    print("------------")
    print(answer)


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------

def main():

    print("=" * 65)
    print("                 AI AGENT")
    print("=" * 65)

    print(
        "\nArchitecture:"
        "\nLLM/Decision -> Tool -> Observation -> Response"
    )

    print(
        "\nAvailable tools:"
        "\n1. get_student_info()"
        "\n2. get_subject_info(subject)"
        "\n3. get_pending_assignments()"
        "\n4. get_low_attendance(threshold)"
        "\n5. get_all_subjects()"
    )

    print(
        "\nDemo mode is enabled."
        "\nType 'exit' to stop.\n"
    )

    while True:

        question = input("Ask the agent: ")

        if question.lower() == "exit":

            print("\nAgent: Goodbye!")
            break

        run_demo_agent(question)


if __name__ == "__main__":
    main()