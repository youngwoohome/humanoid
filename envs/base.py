from abc import ABC, abstractmethod
from core.types import Observation, StepResult


class BaseEnvironment(ABC):
    name: str

    @abstractmethod
    def reset(self) -> Observation:
        pass

    @abstractmethod
    def observe(self) -> Observation:
        pass

    @abstractmethod
    def step(self, action: str) -> StepResult:
        pass

    @abstractmethod
    def is_done(self) -> bool:
        pass

    @abstractmethod
    def render(self) -> str:
        pass

    def look(self) -> StepResult:
        return StepResult(True, "Observed the environment.", self.is_done(), info={"observation": self.observe().state})

    def scan(self, query: str | None = None) -> StepResult:
        return StepResult(True, "Scan returned the current observation.", self.is_done(), info={"query": query})

    def move(self, direction: str) -> StepResult:
        return self.step(f"move_{direction}")

    def pick_up(self, item: str) -> StepResult:
        return self.step("pick_up")

    def unlock(self, target: str, using: str) -> StepResult:
        return self.step("unlock")

    def interact(self, target: str) -> StepResult:
        return self.step("interact")