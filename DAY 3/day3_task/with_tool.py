import os
import json
from dotenv import load_dotenv
from groq import Groq

from tool import get_course_fee


# -----------------------------
# 1. Load API key
# -----------------------------
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "openai/gpt-oss-120b"


# -----------------------------
# 2. System instruction
# -----------------------------
SYSTEM_PROMPT = """
You are a college fee assistant.

Use the get_course_fee tool when the user asks for
an exact course fee.

Never guess a fee.

For general questions, answer briefly without using the tool.
"""


# -----------------------------
# 3. Define the tool
# -----------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": "Get the exact fee of a college course.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "Course code such as CS101"
                    }
                },
                "required": ["course_code"]
            }
        }
    }
]


# -----------------------------
# 4. Ask the LLM
# -----------------------------
def ask_question(question):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    # First LLM call
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0
    )

    assistant_message = response.choices[0].message

    # -----------------------------
    # 5. Check for tool call
    # -----------------------------
    if assistant_message.tool_calls:

        tool_call = assistant_message.tool_calls[0]

        arguments = json.loads(
            tool_call.function.arguments
        )

        print("\n[TOOL CALL]")
        print("Tool:", tool_call.function.name)
        print("Course:", arguments["course_code"])

        # -----------------------------
        # 6. Run Python tool
        # -----------------------------
        result = get_course_fee(
            arguments["course_code"]
        )

        print("[TOOL RESULT]")
        print(result)

        # Add assistant tool request
        messages.append(assistant_message)

        # Add tool result
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })

        # -----------------------------
        # 7. Final LLM response
        # -----------------------------
        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0
        )

        final_answer = (
            final_response
            .choices[0]
            .message
            .content
        )

        return final_answer, True

    # -----------------------------
    # 8. No tool needed
    # -----------------------------
    return assistant_message.content, False


# -----------------------------
# 9. Main program
# -----------------------------
def main():

    print("=" * 50)
    print("COLLEGE FEE ASSISTANT")
    print("=" * 50)

    questions = [
        "What is a college course?",
        "Why is a college course important?",
        "What is the exact fee for CS101?"
    ]

    for question in questions:

        print("\nQUESTION:")
        print(question)

        answer, tool_used = ask_question(question)

        print("\nANSWER:")
        print(answer)

        print("\nTOOL USED:", "YES" if tool_used else "NO")

        print("-" * 50)


if __name__ == "__main__":
    main()