from app.planning.models import Plan, PlanStep
from app.planning.planner import Planner


class FakeLLMClient:
    def generate_structured(
        self,
        prompt: str,
        response_schema: type[Plan],
    ) -> Plan:
        return Plan(
            goal="Compare RAG and fine-tuning",
            steps=[
                PlanStep(
                    id=1,
                    description="Explain RAG",
                ),
                PlanStep(
                    id=2,
                    description="Explain fine-tuning",
                ),
                PlanStep(
                    id=3,
                    description="Compare the two approaches",
                ),
            ],
        )


def test_planner_creates_plan() -> None:
    planner = Planner(FakeLLMClient())

    plan = planner.create_plan(
        "Compare RAG and fine-tuning"
    )

    assert plan.goal == "Compare RAG and fine-tuning"
    assert len(plan.steps) == 3
    assert plan.steps[0].description == "Explain RAG"