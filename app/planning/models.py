from pydantic import BaseModel, Field


class PlanStep(BaseModel):
    id: int = Field(description="The step number.")
    description: str = Field(
        description="What needs to be accomplished in this step."
    )


class Plan(BaseModel):
    goal: str = Field(
        description="The user's overall goal."
    )
    steps: list[PlanStep] = Field(
        description="Ordered steps required to accomplish the goal."
    )

class PlanCompletion(BaseModel):
    complete: bool = Field(
        description=(
            "Whether the overall plan goal has been "
            "adequately accomplished."
        )
    )