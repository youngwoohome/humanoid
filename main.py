# main.py

import argparse

from core.logger import save_episode_log
from core.registry import make_env, make_planner
from core.runner import EpisodeRunner
from harness.executor import ToolExecutor
from harness.validator import ToolValidator
from tools.registry import ToolRegistry


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--max-steps", type=int, default=50)

    args = parser.parse_args()

    env = make_env()
    planner = make_planner(model=args.model)

    runner = EpisodeRunner(
        env=env,
        planner=planner,
        tool_registry=ToolRegistry(),
        validator=ToolValidator(),
        executor=ToolExecutor(),
        max_steps=args.max_steps,
    )

    steps = runner.run()
    success = env.is_done()

    log_path = save_episode_log(
        steps=steps,
        env_name=env.name,
        agent_name=planner.name,
        success=success,
    )

    print("=" * 80)
    print(f"Success: {success}")
    print(f"Saved log to: {log_path}")


if __name__ == "__main__":
    main()

#
# python main.py