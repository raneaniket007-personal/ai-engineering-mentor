from typing import TypedDict

from app.planning.models import Plan


class PlanningGraphState(TypedDict):
    goal: str
    plan: Plan | None
    results: list[str]
    complete: bool
    planning_iterations: int
    termination_reason: str
    error: str | None

def create_initial_state(
    goal: str,
) -> PlanningGraphState:
    return {
        "goal": goal,
        "plan": None,
        "results": [],
        "complete": False,
        "planning_iterations": 0,
        "termination_reason": "",
        "error": None,
    }