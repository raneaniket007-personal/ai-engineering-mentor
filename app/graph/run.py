from app.graph.planning import build_planning_graph
from app.llm.client import LLMClient
from app.graph.state import create_initial_state


def main() -> None:
    llm_client = LLMClient()

    graph = build_planning_graph(
        llm_client,
    )

    result = graph.invoke(create_initial_state("What is RAG?"))

    print("\n--- FINAL RESULT ---")

    for index, output in enumerate(
        result["results"],
        start=1,
    ):
        print(f"\nStep {index}:")
        print(output)


if __name__ == "__main__":
    main()