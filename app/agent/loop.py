from typing import Any
from google.genai import types

from app.tools.registry import TOOLS


class Agent:
    def __init__(self, llm_client: Any) -> None:
        self.llm_client = llm_client
        self.messages: list[types.Content] = []

    def add_user_message(self, message: str) -> None:
        self.messages.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=message)],
            )
        )

    def execute_tool(self, name: str, args: dict[str, Any]) -> Any:
        tool = TOOLS.get(name)

        if tool is None:
            raise ValueError(f"Unknown tool: {name}")

        return tool(**args)

    def run_conversation(self, user_message: str) -> str:
        self.add_user_message(user_message)

        while True:
            # Send entire conversation history to LLM
            response = self.llm_client.generate(self.messages)

            candidate_content = response.candidates[0].content
            # Append model turn (text or function_call) to history
            self.messages.append(candidate_content)

            # Check if model requested a tool call
            has_tool_call = False
            tool_response_parts = []

            for part in candidate_content.parts:
                if part.function_call:
                    has_tool_call = True
                    function_call = part.function_call

                    print(f"Tool requested: {function_call.name}")
                    print(f"Arguments: {function_call.args}")

                    # Execute requested tool
                    result = self.execute_tool(
                        function_call.name,
                        function_call.args,
                    )
                    print(f"Tool result: {result}")

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

            # If no tool calls were requested in this turn, return final text
            if not has_tool_call:
                return response.text or ""