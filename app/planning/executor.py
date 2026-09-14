from app.agent.config import AgentConfig
from app.agent.loop import Agent
from app.llm.client import LLMClient
from app.planning.models import Plan, PlanStep


class PlanExecutor:
    def __init__(self, llm_client: LLMClient, agent_config: AgentConfig | None = None) -> None:
        self.llm_client = llm_client
        self.agent_config = agent_config

    def execute_step(self, plan: Plan, step: PlanStep) -> str:
        prompt = f"""
        You are executing one step of a larger plan.

        Overall goal:
        {plan.goal}

        Current step:
        {step.description}

        Complete this step and provide the result.
        """

        return Agent(self.llm_client, self.agent_config).run_conversation(prompt)

    def execute(self, plan: Plan) -> list[str]:
        return [
            self.execute_step(plan, step)
            for step in plan.steps
        ]