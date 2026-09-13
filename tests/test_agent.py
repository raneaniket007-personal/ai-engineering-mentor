from typing import Any

from google.genai import types

from app.agent.config import AgentConfig
from app.agent.loop import Agent


class FakeLLMClient:
    def generate(
        self,
        messages: list[types.Content],
    ) -> Any:
        return types.GenerateContentResponse(
            candidates=[
                types.Candidate(
                    content=types.Content(
                        role="model",
                        parts=[
                            types.Part.from_text(
                                text="The answer is 4."
                            )
                        ],
                    )
                )
            ]
        )


def test_agent_returns_final_response() -> None:
    agent = Agent(
        llm_client=FakeLLMClient(),
        config=AgentConfig(max_iterations=3),
    )

    result = agent.run_conversation("What is 2 + 2?")

    assert result == "The answer is 4."