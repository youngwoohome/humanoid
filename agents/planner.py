from typing import Any, Dict
import json

from agents.base import BasePlanner
from agents.llm_client import LLMClient
from agents.prompts import build_planner_messages


class PlannerAgent(BasePlanner):
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.name = "planner-llm"
        self.llm = LLMClient(model=model)

    def decide(self, observation, tool_specs, goal) -> Dict[str, Any]:
        messages = build_planner_messages(observation, tool_specs, goal)
        response = self.llm.complete_json(messages)
        return json.loads(response)

    def _decision(self, tool_name, args, next_intent, subgoal) -> Dict[str, Any]:
        return {
            "perception": {
                "summary": next_intent,
                "task_relevant_facts": [next_intent],
            },
            "plan": {
                "current_subgoal": subgoal,
                "next_intent": next_intent,
                "success_condition": "The selected tool call moves the agent closer to the goal.",
            },
            "tool_call": {
                "name": tool_name,
                "args": args,
            },
        }
