import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")

if PROVIDER != "groq":
    raise ValueError("This project is currently configured for Groq.")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY was not found. Check your .env file."
    )

client = Groq(api_key=GROQ_API_KEY)


def ask_llm(prompt, temperature=0):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    print("Provider:", PROVIDER)
    print("Model:", MODEL)
    print("API key loaded:", bool(GROQ_API_KEY))

    answer = ask_llm(
        "What is 25 + 35? Answer briefly."
    )

    print("\nTest response:")
    print(answer)