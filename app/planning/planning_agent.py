from typing import Any

from app.agent.config import AgentConfig
from app.llm.client import LLMClient
from app.planning.evaluator import PlanEvaluator
from app.planning.executor import PlanExecutor
from app.planning.models import Plan
from app.planning.planner import Planner
from app.planning.replanner import Replanner


class PlanningAgent:
    def __init__(
        self,
        llm_client: Any,
        config: AgentConfig | None = None,
    ) -> None:
        self.config = config or AgentConfig()

        self.planner = Planner(llm_client)

        self.executor = PlanExecutor(
            llm_client=llm_client,
            agent_config=self.config,
        )

        self.evaluator = PlanEvaluator(llm_client)

        self.replanner = Replanner(llm_client)

    def run(self, goal: str) -> tuple[Plan, list[str]]:
        plan = self.planner.create_plan(goal)

        for planning_iteration in range(
            self.config.max_iterations
        ):
            print(
                f"\n--- Planning iteration "
                f"{planning_iteration + 1} ---"
            )

            print("\n--- PLAN ---")

            for step in plan.steps:
                print(
                    f"{step.id}. {step.description}"
                )

            results = self.executor.execute(plan)

            complete = self.evaluator.evaluate(
                plan,
                results,
            )

            if complete:
                return plan, results

            print("\nPlan incomplete. Re-planning...")

            plan = self.replanner.replan(
                plan,
                results,
            )

        raise RuntimeError(
            "Planning exceeded maximum iterations."
        )