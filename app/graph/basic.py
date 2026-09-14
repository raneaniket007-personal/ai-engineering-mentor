from langgraph.graph import END, START, StateGraph

from app.graph.state import GraphState


def planner_node(state: GraphState) -> GraphState:
    print("Planner node executing")

    return {
        "message": f"Planning: {state['message']}"
    }


builder = StateGraph(GraphState)

builder.add_node("planner", planner_node)

builder.add_edge(START, "planner")
builder.add_edge("planner", END)

graph = builder.compile()

def main() -> None:
    result = graph.invoke({
        "message": "Learn RAG"
    })

    print(result)


if __name__ == "__main__":
    main()