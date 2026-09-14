from typing import Any

from app.planning.models import Plan, PlanCompletion


class PlanEvaluator:
    def __init__(self, llm_client: Any) -> None:
        self.llm_client = llm_client

    def evaluate(
        self,
        plan: Plan,
        results: list[str],
    ) -> bool:
        summary = "\n\n".join(
            f"Step {step.id}: {result}"
            for step, result in zip(plan.steps, results)
        )

        prompt = f"""
        Evaluate whether the following plan has successfully
        accomplished its goal.

        Goal:
        {plan.goal}

        Plan results:
        {summary}

        Return true if the goal has been adequately accomplished.
        Otherwise return false.
        """

        response = self.llm_client.generate_structured(
            prompt=prompt,
            response_schema=PlanCompletion,
        )

        return response.complete