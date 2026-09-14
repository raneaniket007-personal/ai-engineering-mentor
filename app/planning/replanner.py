from typing import Any

from app.planning.models import Plan


class Replanner:
    def __init__(self, llm_client: Any) -> None:
        self.llm_client = llm_client

    def replan(
        self,
        plan: Plan,
        results: list[str],
    ) -> Plan:
        summary = "\n\n".join(
            f"Step {step.id}: {result}"
            for step, result in zip(plan.steps, results)
        )

        prompt = f"""
        The original plan did not completely accomplish the goal.

        Original goal:
        {plan.goal}

        Original plan:
        {plan.model_dump_json(indent=2)}

        Results so far:
        {summary}

        Create a revised plan that uses what we learned from
        the previous execution.

        Only include remaining work that is necessary.
        """

        return self.llm_client.generate_structured(
            prompt=prompt,
            response_schema=Plan,
        )