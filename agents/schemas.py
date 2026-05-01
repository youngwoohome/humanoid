from typing import List, Literal, Optional

from pydantic import BaseModel


class Perception(BaseModel):
    summary: str
    task_relevant_facts: List[str]


class Plan(BaseModel):
    current_subgoal: str
    next_intent: str
    success_condition: str


class ToolArgs(BaseModel):
    direction: Optional[Literal["north", "south", "east", "west", "forward"]]
    query: Optional[str]
    item: Optional[Literal["key"]]
    target: Optional[Literal["door"]]
    using: Optional[Literal["key"]]


class ToolCall(BaseModel):
    name: Literal["look", "move", "scan", "pick_up", "unlock", "interact"]
    args: ToolArgs


class PlannerDecision(BaseModel):
    perception: Perception
    plan: Plan
    tool_call: ToolCall
