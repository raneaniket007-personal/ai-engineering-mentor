from dataclasses import dataclass


@dataclass
class AgentConfig:
    max_iterations: int = 10
    max_tool_calls: int = 20
    max_tokens: int = 50_000
    max_cost_usd: float = 0.25
    max_duration_seconds: float = 60