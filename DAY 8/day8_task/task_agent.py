"""Day 8 task: College Helpdesk agent with tools, memory, and relevance guard."""
import ast
import operator
import os
from typing import Annotated

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from lc_config import get_vector_store, get_llm, MAX_DISTANCE

# Fees are taken from the training scenario described in the task context.
COURSE_FEES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 0,
}
MAX_LATE_FEE = 2000
LATE_FEE_PER_DAY = 100


@tool
def get_course_fee(course_code: str) -> str:
    """Return the official course fee for a course code such as CS101 or AI202."""
    code = course_code.strip().upper()
    if code not in COURSE_FEES:
        return f"ERROR: No fee information is available for course {code}."
    return f"{code} course fee: Rs. {COURSE_FEES[code]}."


@tool
def calculator(expression: str) -> str:
    """Calculate a basic arithmetic expression containing numbers and +, -, *, /, parentheses."""
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](
                evaluate(node.left), evaluate(node.right)
            )
        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](evaluate(node.operand))
        raise ValueError("Only basic arithmetic is allowed.")

    try:
        result = evaluate(ast.parse(expression, mode="eval"))
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return str(result)
    except Exception as exc:
        return f"ERROR: Invalid calculation: {exc}"


@tool
def check_exam_eligibility(attendance_percent: float) -> str:
    """Check if a student with this attendance percentage (0-100) may write the end-semester exam."""
    if attendance_percent < 0 or attendance_percent > 100:
        return "ERROR: Attendance must be between 0 and 100."
    if attendance_percent >= 75:
        return "ELIGIBLE: You can write the end-semester exam."
    if attendance_percent >= 65:
        return "CONDONATION: You may apply for condonation. Fee: Rs. 500 per course."
    return "NOT ELIGIBLE: Attendance is below 65%."


@tool
def search_handbook(query: str) -> str:
    """Search the college handbook for policy information. If no relevant chunks are found, return NO_MATCH."""
    try:
        store = get_vector_store()
        results = store.similarity_search_with_score(query, k=3)
    except Exception as exc:
        return f"SEARCH_ERROR: {exc}"

    relevant = []
    print(f"\n[search_handbook] query={query!r}")
    for doc, score in results:
        source = doc.metadata.get("source", "unknown")
        print(f"[search_handbook] source={source} distance={score:.4f}")
        if score <= MAX_DISTANCE:
            relevant.append(doc)

    if not relevant:
        return "NO_MATCH: this is not covered in the college handbook."

    return "\n\n".join(
        f"Source: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
        for doc in relevant
    )


@tool
def get_late_fee(days_late: int) -> str:
    """Calculate the late fee. It is Rs. 100 per day, capped at Rs. 2000."""
    if days_late < 0:
        return "ERROR: Days late cannot be negative."
    fee = min(days_late * LATE_FEE_PER_DAY, MAX_LATE_FEE)
    return f"Late fee for {days_late} days: Rs. {fee}."


TOOLS = [
    search_handbook,
    get_course_fee,
    calculator,
    check_exam_eligibility,
    get_late_fee,
]

SYSTEM_PROMPT = f"""
You are the College Helpdesk Agent for Greenfield College of Engineering.
Answer using the handbook and tools. Do not guess policy facts.

Tool instructions:
- Placement questions: call search_handbook.
- Exam eligibility based on attendance: call check_exam_eligibility.
- Course fee questions: call get_course_fee for each course mentioned.
- Fee totals: retrieve the fees, retrieve the late fee when relevant, and use calculator for arithmetic.
- The maximum late fee is Rs. {MAX_LATE_FEE}; the configured late fee is Rs. {LATE_FEE_PER_DAY} per day.
- Follow-up questions must use prior conversation context when it is relevant.
- If search_handbook returns text beginning with NO_MATCH, say you do not know because the answer is not covered in the college handbook. Do not guess.
- Keep answers clear and concise. Show currency as Rs.
"""


def extract_text(message):
    """Get readable text from a LangChain message."""
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    return str(content)


def main():
    llm = get_llm()
    agent = create_react_agent(
        model=llm,
        tools=TOOLS,
        prompt=SYSTEM_PROMPT,
        checkpointer=MemorySaver(),
    )
    config = {"configurable": {"thread_id": "task-run"}}

    # Direct tool tests required by Part B.
    print("=== DIRECT EXAM TOOL TESTS ===")
    for value in [82, 70, 50, 120]:
        print(f"Attendance {value}:",
              check_exam_eligibility.invoke({"attendance_percent": value}))

    questions = [
        "What CGPA do I need to be eligible for placements?",
        "My attendance is 70%. Can I write the exam?",
        "What is the total of the CS101 fee, the AI202 fee and the maximum late fee?",
        "And if I pay only 5 days late instead?",
        "What is the capital of France?",
    ]

    for index, question in enumerate(questions, start=1):
        print("\n" + "#" * 80)
        print(f"QUESTION {index}: {question}")
        result = agent.invoke(
            {"messages": [{"role": "user", "content": question}]},
            config=config,
        )
        messages = result.get("messages", [])
        print("--- Tool calls and messages ---")
        for message in messages:
            name = getattr(message, "name", None)
            tool_calls = getattr(message, "tool_calls", None)
            if tool_calls:
                for call in tool_calls:
                    print(f"TOOL CALL: {call.get('name')} args={call.get('args')}")
            elif name:
                print(f"TOOL RESULT ({name}): {extract_text(message)}")
        if messages:
            print("--- AGENT ANSWER ---")
            print(extract_text(messages[-1]))
        else:
            print("No messages returned by the agent.")

if __name__ == "__main__":
    main()
