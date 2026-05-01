# core/logger.py

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import List

from core.types import EpisodeStep


def save_episode_log(
    steps: List[EpisodeStep],
    env_name: str,
    agent_name: str,
    success: bool,
    output_dir: str = "logs",
) -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = Path(output_dir) / f"{env_name}_{agent_name}_{timestamp}.json"

    payload = {
        "env_name": env_name,
        "agent_name": agent_name,
        "success": success,
        "num_steps": len(steps),
        "steps": [asdict(step) for step in steps],
    }

    with open(path, "w") as f:
        json.dump(payload, f, indent=2)

    return str(path)