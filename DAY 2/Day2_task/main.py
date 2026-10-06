# main.py

from direct_prompting import direct_prompt
from chain_of_thought import chain_of_thought
from react_agent import react_agent
from self_consistency import run_multiple_times


def main():

    while True:

        print("\n")
        print("=" * 60)
        print("DAY 2 - REASONING AND ACTING")
        print("=" * 60)

        print("1. Direct Prompting")
        print("2. Chain-of-Thought")
        print("3. ReAct Agent")
        print("4. Self-Consistency")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            question = input("\nEnter question: ")

            result = direct_prompt(question)

            print("\nFinal Answer:")
            print(result)

        elif choice == "2":

            question = input("\nEnter question: ")

            result = chain_of_thought(question)

            print("\nFinal Answer:")
            print(result)

        elif choice == "3":

            question = input("\nEnter question: ")

            react_agent(question)

        elif choice == "4":

            run_multiple_times()

        elif choice == "5":

            print("\nProgram ended.")

            break

        else:

            print("\nInvalid choice.")


if __name__ == "__main__":
    main()