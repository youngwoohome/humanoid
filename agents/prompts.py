# agents/prompts.py

import json
from dataclasses import asdict

from core.types import Observation


PLANNER_PROMPT = """
You are the PlannerAgent for an embodied LLM agent.

Your job is to:
1. interpret the current observation,
2. identify task-relevant facts,
3. choose the current subgoal,
4. select exactly one tool call.

You cannot directly change the world.
You must choose one tool from the available tool list.

Return valid JSON only:
{
  "perception": {
    "summary": "...",
    "task_relevant_facts": []
  },
  "plan": {
    "current_subgoal": "...",
    "next_intent": "...",
    "success_condition": "..."
  },
  "tool_call": {
    "name": "...",
    "args": {}
  }
}
""".strip()

SYSTEM_PROMPT = PLANNER_PROMPT


def build_messages(observation: Observation):
    return [
        {
            "role": "system",
            "content": PLANNER_PROMPT,
        },
        {
            "role": "user",
            "content": f"""
Current observation:

{asdict(observation)}
""".strip(),
        },
    ]


def build_planner_messages(observation, tool_specs, goal):
    return [
        {"role": "system", "content": PLANNER_PROMPT},
        {
            "role": "user",
            "content": json.dumps(
                {
                    "observation": asdict(observation),
                    "tool_specs": tool_specs,
                    "goal": goal,
                },
                indent=2,
            ),
        },
    ]