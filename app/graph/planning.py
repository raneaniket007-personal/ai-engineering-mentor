from app.graph.safe_node import safe_node
from typing import Any

from langgraph.graph import END, START, StateGraph

from app.graph.nodes import PlanningGraphNodes
from app.graph.state import PlanningGraphState

MAX_PLANNING_ITERATIONS = 3

def route_after_evaluation(
    state: PlanningGraphState,
) -> str:
    if state["error"]:
        return "error"

    if state["complete"]:
        return "complete"

    if (
        state["planning_iterations"]
        >= MAX_PLANNING_ITERATIONS
    ):
        return "max_iterations"

    return "replan"

def route_after_planner(
    state: PlanningGraphState,
) -> str:
    if state["error"]:
        return "error"

    return "executor"

def route_after_executor(
    state: PlanningGraphState,
) -> str:
    if state["error"]:
        return "error"

    return "evaluator"

def route_after_replanner(
    state: PlanningGraphState,
) -> str:
    if state["error"]:
        return "error"

    return "executor"

def build_planning_graph(
    llm_client: Any,
):
    nodes = PlanningGraphNodes(
        llm_client,
    )

    builder = StateGraph(
        PlanningGraphState,
    )

    builder.add_node(
        "planner",
        safe_node(nodes.plan),
    )

    builder.add_node(
        "executor",
        safe_node(nodes.execute),
    )

    builder.add_node(
        "evaluator",
        safe_node(nodes.evaluate),
    )

    builder.add_node(
        "replanner",
        safe_node(nodes.replan),
    )

    builder.add_node(
        "complete",
        nodes.complete,
    )

    builder.add_node(
        "max_iterations",
        nodes.max_iterations,
    )

    builder.add_node(
        "error",
        nodes.handle_error,
    )

    builder.add_edge(
        START,
        "planner",
    )

    builder.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "error": "error",
            "executor": "executor",
        },
    )

    builder.add_conditional_edges(
        "executor",
        route_after_executor,
        {
            "evaluator": "evaluator",
            "error": "error",
        },
    )

    builder.add_conditional_edges(
        "evaluator",
        route_after_evaluation,
        {
            "complete": "complete",
            "replan": "replanner",
            "max_iterations": "max_iterations",
            "error": "error",
        },
    )

    builder.add_conditional_edges(
        "replanner",
        route_after_replanner,
        {
            "executor": "executor",
            "error": "error",
        },
    )

    builder.add_edge(
        "complete",
        END,
    )

    builder.add_edge(
        "max_iterations",
        END,
    )

    builder.add_edge(
        "error",
        END,
    )

    return builder.compile()