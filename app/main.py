from app.agent.config import AgentConfig
from app.agent.loop import Agent
from app.llm.client import LLMClient
from app.planning.planning_agent import PlanningAgent


def main() -> None:
    agent = PlanningAgent(LLMClient(), AgentConfig(max_iterations=10))


    while True:
        user_message = input("You: ")

        if user_message.lower() == "exit":
            break

        # response = mentor.run_conversation(user_message)

        # print(f"\nMentor: {response}\n")
        plan, results = agent.run(user_message)

        print("\n--- RESULTS ---")

        for index, result in enumerate(results, start=1):
            print(f"\nStep {index}:")
            print(result)


if __name__ == "__main__":
    main()