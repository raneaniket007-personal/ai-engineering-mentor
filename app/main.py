from app.llm.client import LLMClient


def main() -> None:
    mentor = LLMClient()

    print("AI Engineering Mentor")
    print("Type 'exit' to quit.\n")

    while True:
        user_message = input("You: ")

        if user_message.lower() == "exit":
            break

        response = mentor.generate(user_message)

        print(f"\nMentor: {response}\n")


if __name__ == "__main__":
    main()