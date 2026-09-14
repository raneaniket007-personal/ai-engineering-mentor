from typing import Any

from app.planning.models import Plan


class Planner:
    def __init__(self, llm_client: Any) -> None:
        self.llm_client = llm_client

    def create_plan(self, goal: str) -> Plan:
        prompt = f"""
        Create a plan to accomplish the following goal:

        {goal}

        Break the goal into clear, ordered steps.
        Only include steps that are necessary to accomplish the goal.
        """

        response = self.llm_client.generate_structured(
            prompt=prompt,
            response_schema=Plan,
        )

        return response