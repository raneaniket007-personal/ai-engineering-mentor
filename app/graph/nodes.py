from typing import Any

from app.planning.evaluator import PlanEvaluator
from app.planning.executor import PlanExecutor
from app.planning.planner import Planner
from app.planning.replanner import Replanner

from app.graph.state import PlanningGraphState


class PlanningGraphNodes:
    def __init__(
        self,
        llm_client: Any,
    ) -> None:
        self.planner = Planner(llm_client)

        self.executor = PlanExecutor(
            llm_client=llm_client,
        )

        self.evaluator = PlanEvaluator(
            llm_client,
        )

        self.replanner = Replanner(
            llm_client,
        )

    def plan(
        self,
        state: PlanningGraphState,
    ) -> dict:
        print("\n--- Planner node ---")

        plan = self.planner.create_plan(
            state["goal"],
        )

        print("\n--- PLAN ---")

        for step in plan.steps:
            print(
                f"{step.id}. {step.description}"
            )

        return {
            "plan": plan,
            "planning_iterations": 1,
        }

    def execute(
        self,
        state: PlanningGraphState,
    ) -> dict:
        print("\n--- Executor node ---")

        plan = state["plan"]

        if plan is None:
            raise RuntimeError(
                "Cannot execute without a plan."
            )

        results = self.executor.execute(plan)

        return {
            "results": results,
        }

    def evaluate(
        self,
        state: PlanningGraphState,
    ) -> dict:
        print("\n--- Evaluator node ---")

        plan = state["plan"]

        if plan is None:
            raise RuntimeError(
                "Cannot evaluate without a plan."
            )

        complete = self.evaluator.evaluate(
            plan,
            state["results"],
        )

        print(
            f"Plan complete: {complete}"
        )

        return {
            "complete": complete,
        }

    def replan(
        self,
        state: PlanningGraphState,
    ) -> dict:
        print("\n--- Replanner node ---")

        plan = state["plan"]

        if plan is None:
            raise RuntimeError(
                "Cannot replan without a plan."
            )

        new_plan = self.replanner.replan(
            plan,
            state["results"],
        )

        print("\n--- NEW PLAN ---")

        for step in new_plan.steps:
            print(
                f"{step.id}. {step.description}"
            )

        return {
            "plan": new_plan,
            "planning_iterations": (
                state["planning_iterations"] + 1
            ),
        }

    def complete(
        self,
        state: PlanningGraphState,
    ) -> dict:
        print("\n--- Goal completed ---")

        return {
            "termination_reason": "completed",
        }


    def max_iterations(
        self,
        state: PlanningGraphState,
    ) -> dict:
        print(
            "\n--- Maximum planning iterations reached ---"
        )

        return {
            "termination_reason": "max_iterations",
        }

    def handle_error(
        self,
        state: PlanningGraphState,
    ) -> dict:
        print("\n--- Graph execution failed ---")
        print(f"Error: {state['error']}")
        return {
            "termination_reason": "error",
        }