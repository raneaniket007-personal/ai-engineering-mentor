from typing import Any

from google.genai import types

from app.agent.executor import ToolExecutor
from app.graph.agent_state import AgentGraphState


class AgentGraphNodes:
    def __init__(
        self,
        llm_client: Any,
    ) -> None:
        self.llm_client = llm_client
        self.tool_executor = ToolExecutor()

    def model(
        self,
        state: AgentGraphState,
    ) -> dict:
        response = self.llm_client.generate(
            state["messages"]
        )

        candidate_content = (
            response.candidates[0].content
        )

        return {
            "messages": (
                state["messages"]
                + [candidate_content]
            )
        }

    def execute_tools(
        self,
        state: AgentGraphState,
    ) -> dict:
        latest_message = state["messages"][-1]

        tool_response_parts = []

        for part in latest_message.parts:
            if not part.function_call:
                continue

            function_call = part.function_call

            print(
                f"Tool requested: "
                f"{function_call.name}"
            )

            print(
                f"Arguments: "
                f"{function_call.args}"
            )

            try:
                result = self.tool_executor.execute(
                    function_call.name,
                    function_call.args,
                )

                print(
                    f"Tool result: {result}"
                )

                tool_response_parts.append(
                    types.Part(
                        function_response=(
                            types.FunctionResponse(
                                name=function_call.name,
                                response={
                                    "result": result
                                },
                                id=getattr(
                                    function_call,
                                    "id",
                                    None,
                                ),
                            )
                        )
                    )
                )

            except Exception as exc:
                error_message = str(exc)

                print(
                    f"Tool error: "
                    f"{error_message}"
                )

                tool_response_parts.append(
                    types.Part(
                        function_response=(
                            types.FunctionResponse(
                                name=function_call.name,
                                response={
                                    "error": error_message
                                },
                                id=getattr(
                                    function_call,
                                    "id",
                                    None,
                                ),
                            )
                        )
                    )
                )

        tool_response = types.Content(
            role="user",
            parts=tool_response_parts,
        )

        return {
            "messages": (
                state["messages"]
                + [tool_response]
            )
        }

    def finalize(
        self,
        state: AgentGraphState,
    ) -> dict:
        latest_message = state["messages"][-1]

        text_parts = [
            part.text
            for part in latest_message.parts
            if part.text
        ]

        return {
            "final_response": "\n".join(
                text_parts
            )
        }