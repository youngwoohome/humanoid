from typing import Any, Dict

from agents.base import BasePlanner
from agents.llm_client import LLMClient
from agents.prompts import build_planner_messages
from agents.schemas import PlannerDecision


class PlannerAgent(BasePlanner):
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.name = "planner-llm"
        self.llm = LLMClient(model=model)

    def decide(self, observation, tool_specs, goal) -> Dict[str, Any]:
        messages = build_planner_messages(observation, tool_specs, goal)
        decision = self.llm.run_llm(messages, PlannerDecision)
        payload = decision.model_dump(exclude_none=True)
        payload["tool_call"]["args"] = self._tool_args(
            payload["tool_call"]["name"],
            payload["tool_call"].get("args", {}),
        )
        return payload

    def _tool_args(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        allowed_args = {
            "look": set(),
            "move": {"direction"},
            "scan": {"query"},
            "pick_up": {"item"},
            "unlock": {"target", "using"},
            "interact": {"target"},
        }
        return {
            key: value
            for key, value in args.items()
            if key in allowed_args.get(tool_name, set())
        }