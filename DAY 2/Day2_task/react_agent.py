# react_agent.py

from llm_client import ask_llm
from tools import get_course_fee, calculator


def choose_tool(question):

    prompt = f"""
You are deciding which tool a ReAct agent should use.

Question:
{question}

Available tools:

get_course_fee:
Retrieves the exact fee of a course.

calculator:
Performs arithmetic.

none:
Use when no tool is required.

Return exactly:

TOOL=<tool name>
ARGUMENT=<argument>

Examples:

TOOL=get_course_fee
ARGUMENT=CS101

TOOL=calculator
ARGUMENT=45000*3

TOOL=none
ARGUMENT=none
"""

    return ask_llm(prompt, temperature=0)


def parse_tool_response(response):

    tool = "none"
    argument = "none"

    for line in response.splitlines():

        line = line.strip()

        if line.startswith("TOOL="):
            tool = line.split("=", 1)[1].strip()

        elif line.startswith("ARGUMENT="):
            argument = line.split("=", 1)[1].strip()

    return tool, argument


def execute_tool(tool, argument):

    if tool == "get_course_fee":

        return get_course_fee(argument)

    elif tool == "calculator":

        return calculator(argument)

    else:

        return "No external tool was required."


def react_agent(question):

    print("=" * 60)
    print("REACT AGENT")
    print("=" * 60)

    # THOUGHT
    print("\n[THOUGHT]")
    print("The agent analyzes the question and determines whether external information is required.")

    decision = choose_tool(question)

    tool, argument = parse_tool_response(decision)

    print("\n[THOUGHT]")
    print(f"Selected tool: {tool}")
    print(f"Required input: {argument}")

    # ACTION
    if tool != "none":

        print("\n[ACTION]")
        print(f"Calling {tool} with: {argument}")

        observation = execute_tool(tool, argument)

    else:

        print("\n[ACTION]")
        print("No tool call")

        observation = "No tool result."

    # OBSERVATION
    print("\n[OBSERVATION]")
    print(observation)

    # FINAL ANSWER
    final_prompt = f"""
You are a college fee assistant.

User question:
{question}

The ReAct agent obtained this tool observation:

{observation}

Answer the user using the observation.

Rules:
- Never invent a course fee.
- If the tool returned an error, clearly say that the course was not found.
- Keep the answer simple.
"""

    final_answer = ask_llm(final_prompt, temperature=0)

    print("\n[FINAL ANSWER]")
    print(final_answer)

    return final_answer


if __name__ == "__main__":

    question = input("\nEnter your question: ")

    react_agent(question)