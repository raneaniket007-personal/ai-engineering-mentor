from google.genai import types

from app.graph.agent import build_agent_graph
from app.llm.client import LLMClient


def main() -> None:
    llm_client = LLMClient()

    graph = build_agent_graph(
        llm_client,
    )

    user_message = types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text="What is RAG?"
            )
        ],
    )

    config = {
        "configurable": {
            "thread_id": "demo-thread-1"
        }
    }

    result = graph.invoke(
        {
            "messages": [user_message],
            "final_response": "",
        },
        config=config,
    )

    snapshot = graph.get_state(config)

    print("\n--- CHECKPOINT STATE ---")
    print(snapshot.values)

    print("\n--- FINAL RESPONSE ---")
    print(result["final_response"])


if __name__ == "__main__":
    main()