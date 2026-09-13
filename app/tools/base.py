from dataclasses import dataclass
from typing import Any, Callable

from pydantic import BaseModel


@dataclass
class ToolDefinition:
    name: str
    description: str
    function: Callable[..., Any]
    args_schema: type[BaseModel]