import os
from dotenv import load_dotenv
from groq import Groq


# --------------------------------
# 1. Load API key
# --------------------------------
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# --------------------------------
# 2. Model
# --------------------------------
MODEL = "openai/gpt-oss-120b"


# --------------------------------
# 3. System prompt
# --------------------------------
SYSTEM_PROMPT = """
You are a simple college fee assistant.

Answer every question in 1 or 2 short sentences.

You do NOT have access to any external database or tools.

If the user asks for an exact course fee, do not guess.
Clearly say that the exact fee cannot be verified.
"""


# --------------------------------
# 4. Ask the LLM
# --------------------------------
def ask_question(question):

    response = client.chat.completions.create(
        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ],

        temperature=0
    )

    return response.choices[0].message.content


# --------------------------------
# 5. Main program
# --------------------------------
def main():

    print("=" * 50)
    print("COLLEGE FEE ASSISTANT")
    print("PLAIN LLM - NO TOOL")
    print("=" * 50)

    questions = [
        "What is a college course?",
        "Why is a college course important?",
        "What is the exact fee for CS101?"
    ]

    for i, question in enumerate(questions, start=1):

        print(f"\nQUESTION {i}")
        print(question)

        answer = ask_question(question)

        print("\nANSWER")
        print(answer)

        print("-" * 50)


if __name__ == "__main__":
    main()