from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class Observation:
    world_type: str
    goal: str
    state: Dict[str, Any]
    valid_actions: List[str]
    previous_feedback: Optional[str] = None


@dataclass
class ValidationResult:
    approved: bool
    reason: str = ""


@dataclass
class StepResult:
    success: bool
    message: str
    done: bool
    reward: float = 0.0
    info: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EpisodeStep:
    step: int
    observation: Dict[str, Any]
    decision: Dict[str, Any]
    result: Dict[str, Any]
    validation: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EpisodeLog:
    env_name: str
    agent_name: str
    goal: str
    success: bool
    steps: List[EpisodeStep]
