# self_consistency.py

from collections import Counter
from llm_client import ask_llm


QUESTION = """
A student has 3 subjects.

Subject 1 = 80 marks
Subject 2 = 70 marks
Subject 3 = 90 marks

What is the average mark?
"""


def run_multiple_times():

    answers = []

    print("=" * 60)
    print("SELF-CONSISTENCY EXPERIMENT")
    print("=" * 60)

    for i in range(5):

        prompt = f"""
Solve this problem carefully.

{QUESTION}

Give only the final numerical answer.
"""

        answer = ask_llm(
            prompt,
            temperature=0.7
        )

        answers.append(answer)

        print(f"\nRun {i + 1}")
        print(answer)

    return answers


def majority_answer(answers):

    cleaned = [
        answer.strip().lower()
        for answer in answers
    ]

    counter = Counter(cleaned)

    return counter.most_common(1)[0]


def temperature_zero():

    prompt = f"""
Solve this problem.

{QUESTION}

Give only the final numerical answer.
"""

    return ask_llm(
        prompt,
        temperature=0
    )


if __name__ == "__main__":

    answers = run_multiple_times()

    majority, count = majority_answer(answers)

    print("\n" + "=" * 60)
    print("MAJORITY ANSWER")
    print("=" * 60)

    print("Answer:", majority)
    print("Count:", count)

    print("\n" + "=" * 60)
    print("TEMPERATURE = 0")
    print("=" * 60)

    result = temperature_zero()

    print(result)