from typing import Any, TypedDict


class AgentGraphState(TypedDict):
    messages: list[Any]
    final_response: str