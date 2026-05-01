# core/runner.py

from dataclasses import asdict
from typing import List

from agents.planner import PlannerAgent
from envs.base import BaseEnvironment
from core.types import EpisodeStep
from harness.executor import ToolExecutor
from harness.validator import ToolValidator
from tools.registry import ToolRegistry


class EpisodeRunner:
    def __init__(
        self,
        env: BaseEnvironment,
        planner: PlannerAgent,
        tool_registry: ToolRegistry,
        validator: ToolValidator,
        executor: ToolExecutor,
        max_steps: int = 50,
    ):
        self.env = env
        self.planner = planner
        self.tool_registry = tool_registry
        self.validator = validator
        self.executor = executor
        self.max_steps = max_steps

    def run(self) -> List[EpisodeStep]:
        steps = []

        observation = self.env.reset()

        for step_idx in range(1, self.max_steps + 1):
            print("=" * 80)
            print(f"Step {step_idx}")
            print(self.env.render())

            decision = self.planner.decide(
                observation=observation,
                tool_specs=self.tool_registry.specs(),
                goal=self.env.goal,
            )
            tool_call = decision["tool_call"]

            validation = self.validator.validate(
                tool_call=tool_call,
                tool_registry=self.tool_registry,
                env=self.env,
            )

            if not validation.approved:
                result = self.executor.execute(
                    {"name": "look", "args": {}},
                    env=self.env,
                )
                result.success = False
                result.message = validation.reason
            else:
                result = self.executor.execute(
                    tool_call=tool_call,
                    env=self.env,
                )

            new_observation = self.env.observe()
            new_observation.previous_feedback = result.message

            steps.append(
                EpisodeStep(
                    step=step_idx,
                    observation=asdict(observation),
                    decision=decision,
                    validation=asdict(validation),
                    result=asdict(result),
                )
            )

            print(f"Subgoal: {decision['plan']['current_subgoal']}")
            print(f"Tool: {tool_call['name']}({tool_call.get('args', {})})")
            print(f"Validation: {validation.reason}")
            print(f"Result: {result.message}")

            observation = new_observation

            if result.done:
                print("Goal completed!")
                break

        return steps