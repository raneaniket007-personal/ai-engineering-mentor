from typing import Any
from google.genai import types

from app.agent.config import AgentConfig
from app.agent.events import AgentEvent
from app.agent.executor import ToolExecutor


class Agent:
    def __init__(
        self,
        llm_client: Any,
        config: AgentConfig | None = None,
    ) -> None:
        self.llm_client = llm_client
        self.config = config or AgentConfig()
        self.tool_executor = ToolExecutor()
        self.messages: list[types.Content] = []
    
    def emit_event(self, event: AgentEvent) -> None:
        if event.type == "tool_call":
            print(
                f"Tool requested: {event.data['name']}"
            )
            print(
                f"Arguments: {event.data['args']}"
            )

        elif event.type == "tool_result":
            print(
                f"Tool result: {event.data['result']}"
            )

        elif event.type == "tool_error":
            print(
                f"Tool error: {event.data['error']}"
            )

    def add_user_message(self, message: str) -> None:
        self.messages.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=message)],
            )
        )

    def run_conversation(self, user_message: str) -> str:
        self.add_user_message(user_message)

        for iteration in range(self.config.max_iterations):
            response = self.llm_client.generate(self.messages)

            candidate_content = response.candidates[0].content

            self.messages.append(candidate_content)

            has_tool_call = False
            tool_response_parts = []

            for part in candidate_content.parts:
                if not part.function_call:
                    continue

                has_tool_call = True

                function_call = part.function_call

                self.emit_event(
                    AgentEvent(
                        type="tool_call",
                        data={
                            "name": function_call.name,
                            "args": dict(function_call.args),
                        },
                    )
                )

                try:
                    result = self.tool_executor.execute(
                        function_call.name,
                        dict(function_call.args),
                    )

                    self.emit_event(
                        AgentEvent(
                            type="tool_result",
                            data={
                                "name": function_call.name,
                                "result": result,
                            },
                        )
                    )

                except Exception as exc:
                    error_message = str(exc)

                    self.emit_event(
                        AgentEvent(
                            type="tool_error",
                            data={
                                "name": function_call.name,
                                "error": error_message,
                            },
                        )
                    )

                    result = {
                        "error": error_message,
                    }

                tool_response_parts.append(
                    types.Part(
                            function_response=types.FunctionResponse(
                                name=function_call.name,
                                response={"result": result},
                                id=getattr(function_call, "id", None),
                            )
                        )
                )

            if tool_response_parts:
                self.messages.append(
                    types.Content(
                        role="user",
                        parts=tool_response_parts,
                    )
                )

            if not has_tool_call:
                return response.text or ""

        raise RuntimeError(
            f"Agent exceeded maximum iterations: "
            f"{self.config.max_iterations}"
        )