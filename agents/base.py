from abc import ABC, abstractmethod
from typing import Any, Dict


class BasePlanner(ABC):
    name: str

    @abstractmethod
    def decide(self, observation, tool_specs, goal) -> Dict[str, Any]:
        pass