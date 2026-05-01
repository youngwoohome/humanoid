# core/registry.py

from agents.planner import PlannerAgent

from envs.grid2d import Grid2DWorld


def make_env():
    return Grid2DWorld()


def make_planner(model: str = "gpt-4o-mini"):
    return PlannerAgent(model=model)