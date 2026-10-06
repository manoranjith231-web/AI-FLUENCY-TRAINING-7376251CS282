# direct_prompting.py

from llm_client import ask_llm


def direct_prompt(question):

    prompt = f"""
You are a college fee assistant.

Answer the user's question directly.

Do not use any external tools.
Do not show your internal reasoning.

Question:
{question}

Give a short and clear answer.
"""

    return ask_llm(prompt, temperature=0)


if __name__ == "__main__":

    question = input("Enter your question: ")

    answer = direct_prompt(question)

    print("\nDIRECT PROMPTING")
    print("----------------")
    print(answer)