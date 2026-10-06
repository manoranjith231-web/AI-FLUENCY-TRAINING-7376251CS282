# chain_of_thought.py

from llm_client import ask_llm


def chain_of_thought(question):

    prompt = f"""
You are a college fee assistant.

Solve the following problem carefully using
step-by-step reasoning internally.

Do not use external tools.

Do not reveal private chain-of-thought.
Instead, provide:
1. A brief explanation of the reasoning.
2. The final answer.

Question:
{question}
"""

    return ask_llm(prompt, temperature=0)


if __name__ == "__main__":

    question = input("Enter your reasoning question: ")

    answer = chain_of_thought(question)

    print("\nCHAIN-OF-THOUGHT APPROACH")
    print("------------------------")
    print(answer)