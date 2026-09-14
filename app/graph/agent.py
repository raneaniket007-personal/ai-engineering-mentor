from typing import Any

from langgraph.graph import END, START, StateGraph

from app.graph.agent_nodes import AgentGraphNodes
from app.graph.agent_state import AgentGraphState

from langgraph.checkpoint.memory import InMemorySaver

def route_after_model(
    state: AgentGraphState,
) -> str:
    latest_message = state["messages"][-1]

    for part in latest_message.parts:
        if part.function_call:
            return "tools"

    return "final"


def build_agent_graph(
    llm_client: Any,
):
    nodes = AgentGraphNodes(
        llm_client,
    )

    builder = StateGraph(
        AgentGraphState,
    )

    builder.add_node(
        "model",
        nodes.model,
    )

    builder.add_node(
        "tools",
        nodes.execute_tools,
    )

    builder.add_node(
        "final",
        nodes.finalize,
    )

    builder.add_edge(
        START,
        "model",
    )

    builder.add_conditional_edges(
        "model",
        route_after_model,
        {
            "tools": "tools",
            "final": "final",
        },
    )

    builder.add_edge(
        "tools",
        "model",
    )

    builder.add_edge(
        "final",
        END,
    )

    checkpointer = InMemorySaver()

    return builder.compile(
        checkpointer=checkpointer,
    )