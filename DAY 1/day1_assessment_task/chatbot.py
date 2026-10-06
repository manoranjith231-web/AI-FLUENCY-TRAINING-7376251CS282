"""
Plain Chatbot
--------------
This system demonstrates an LLM-style chatbot without
private-data access or external tools.

Architecture:

User -> Chatbot -> Response
"""


def chatbot(user_input):
    """
    Generate a generic response.

    This chatbot does NOT access student_data.json.
    """

    text = user_input.lower()

    if "hello" in text or "hi" in text:
        return "Hello! I am a plain chatbot. How can I help you?"

    if "what can you do" in text:
        return (
            "I can understand your questions and generate responses, "
            "but I cannot directly access your private student records."
        )

    if "dbms" in text or "marks" in text or "attendance" in text:
        return (
            "I can discuss academic topics, but I do not have access "
            "to your private academic data."
        )

    return (
        "I can generate a response using the information available "
        "to me, but I do not have access to your private student file."
    )


def main():
    print("=" * 55)
    print("             PLAIN CHATBOT")
    print("=" * 55)

    print("\nThis chatbot does NOT access private student data.")
    print("Type 'exit' to stop.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        response = chatbot(user_input)

        print("Chatbot:", response)


if __name__ == "__main__":
    main()