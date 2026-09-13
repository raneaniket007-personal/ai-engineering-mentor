from typing import Any

from pydantic import ValidationError

from app.tools.registry import TOOLS


class ToolExecutor:
    def execute(self, name: str, args: dict[str, Any]) -> Any:
        tool = TOOLS.get(name)

        if tool is None:
            raise ValueError(f"Unknown tool: {name}")

        try:
            validated_args = tool.args_schema.model_validate(args)
        except ValidationError as exc:
            raise ValueError(
                f"Invalid arguments for tool '{name}': {exc}"
            ) from exc

        return tool.function(**validated_args.model_dump())