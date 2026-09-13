from app.agent.config import AgentConfig
from app.agent.loop import Agent
from app.llm.client import LLMClient


def main() -> None:
    mentor = Agent(LLMClient(), config=AgentConfig(max_iterations=10),)

    print("AI Engineering Mentor")
    print("Type 'exit' to quit.\n")

    while True:
        user_message = input("You: ")

        if user_message.lower() == "exit":
            break

        response = mentor.run_conversation(user_message)

        print(f"\nMentor: {response}\n")


if __name__ == "__main__":
    main()