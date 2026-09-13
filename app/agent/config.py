from dataclasses import dataclass


@dataclass
class AgentConfig:
    max_iterations: int = 10