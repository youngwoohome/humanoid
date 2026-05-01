# envs/grid2d.py

from typing import List, Tuple
from core.types import Observation, StepResult
from envs.base import BaseEnvironment


class Grid2DWorld(BaseEnvironment):
    name = "grid2d"

    VALID_ACTIONS = [
        "move_north",
        "move_south",
        "move_east",
        "move_west",
        "look",
        "pick_up",
        "unlock",
    ]

    def __init__(self, map_path: str = "maps/grid_escape_room.txt"):
        self.map_path = map_path
        self.goal = "Find the key, unlock the door, and reach the goal."
        self.grid = []
        self.agent_pos = (0, 0)
        self.inventory = []
        self.done = False

    def reset(self) -> Observation:
        self.grid = self._load_map(self.map_path)
        self.agent_pos = self._find_symbol("A")
        self.inventory = []
        self.done = False
        return self.observe()

    def observe(self) -> Observation:
        return Observation(
            world_type="grid_2d",
            goal=self.goal,
            state={
                "position": list(self.agent_pos),
                "inventory": self.inventory,
                "visible_map": self._render_grid_lines(),
                "legend": {
                    "A": "agent",
                    "#": "wall",
                    ".": "empty space",
                    "K": "key",
                    "D": "locked door",
                    "G": "goal",
                },
            },
            valid_actions=self.VALID_ACTIONS,
        )

    def step(self, action: str) -> StepResult:
        if action == "look":
            return StepResult(
                success=True,
                message="You look around.",
                done=self.done,
            )

        if action.startswith("move_"):
            return self._move(action)

        if action == "pick_up":
            return self._pick_up()

        if action == "unlock":
            return self._unlock()

        return StepResult(
            success=False,
            message=f"Unknown action: {action}",
            done=self.done,
        )

    def can_execute_tool(self, name: str, args: dict) -> tuple[bool, str]:
        if name in {"look", "scan"}:
            return True, "Allowed."

        if name == "move":
            direction = args.get("direction")
            if direction == "forward":
                direction = "east"
            next_pos = self._next_position(direction)
            if next_pos is None:
                return False, f"Unsupported direction: {args.get('direction')}"
            r, c = next_pos
            target = self.grid[r][c]
            if target == "#":
                return False, f"Cannot move {direction}: blocked by a wall."
            if target == "D" and "key" not in self.inventory:
                return False, "Cannot move through the locked door without a key."
            return True, "Allowed."

        if name == "pick_up":
            item = args.get("item")
            if item != "key":
                return False, f"Unknown item: {item}"
            return True, "Allowed."

        if name == "unlock":
            if args.get("using") != "key":
                return False, "The door must be unlocked using the key."
            if "key" not in self.inventory:
                return False, "Cannot unlock the door before picking up the key."
            return True, "Allowed."

        if name == "interact":
            return True, "Allowed."

        return False, f"Tool not supported by Grid2DWorld: {name}"

    def move(self, direction: str) -> StepResult:
        if direction == "forward":
            direction = "east"
        return self._move(f"move_{direction}")

    def look(self) -> StepResult:
        return StepResult(
            success=True,
            message="You look around.",
            done=self.done,
            info={"observation": self.observe().state},
        )

    def scan(self, query: str | None = None) -> StepResult:
        objects = self._nearby_objects()
        if query:
            objects = [obj for obj in objects if query.lower() in obj.lower()]
        return StepResult(
            success=True,
            message=f"Scan found: {objects or 'nothing relevant'}.",
            done=self.done,
            info={"objects": objects},
        )

    def pick_up(self, item: str) -> StepResult:
        if item != "key":
            return StepResult(False, f"There is no {item} nearby.", self.done)
        return self._pick_up()

    def unlock(self, target: str, using: str) -> StepResult:
        if target != "door":
            return StepResult(False, f"There is no {target} to unlock.", self.done)
        if using != "key":
            return StepResult(False, f"Cannot unlock the door using {using}.", self.done)
        return self._unlock()

    def interact(self, target: str) -> StepResult:
        return StepResult(False, f"Nothing happens when interacting with {target}.", self.done)

    def is_done(self) -> bool:
        return self.done

    def render(self) -> str:
        return "\n".join(self._render_grid_lines())

    def _load_map(self, path: str) -> List[List[str]]:
        with open(path, "r") as f:
            return [list(line.rstrip("\n")) for line in f.readlines()]

    def _find_symbol(self, symbol: str) -> Tuple[int, int]:
        for r, row in enumerate(self.grid):
            for c, value in enumerate(row):
                if value == symbol:
                    return (r, c)
        raise ValueError(f"Symbol {symbol} not found in map.")

    def _render_grid_lines(self) -> List[str]:
        lines = []
        for r, row in enumerate(self.grid):
            line = ""
            for c, value in enumerate(row):
                if (r, c) == self.agent_pos:
                    line += "A"
                else:
                    if value == "A":
                        line += "."
                    else:
                        line += value
            lines.append(line)
        return lines

    def _next_position(self, direction: str) -> Tuple[int, int] | None:
        deltas = {
            "north": (-1, 0),
            "south": (1, 0),
            "east": (0, 1),
            "west": (0, -1),
        }
        if direction not in deltas:
            return None
        dr, dc = deltas[direction]
        r, c = self.agent_pos
        return (r + dr, c + dc)

    def _nearby_objects(self) -> List[str]:
        r, c = self.agent_pos
        objects = []
        positions = {
            "current": (r, c),
            "north": (r - 1, c),
            "south": (r + 1, c),
            "west": (r, c - 1),
            "east": (r, c + 1),
        }
        labels = {"K": "key", "D": "door", "G": "goal"}
        for direction, (pr, pc) in positions.items():
            symbol = self.grid[pr][pc]
            if symbol in labels:
                objects.append(f"{labels[symbol]}:{direction}")
        return objects

    def _move(self, action: str) -> StepResult:
        deltas = {
            "move_north": (-1, 0),
            "move_south": (1, 0),
            "move_east": (0, 1),
            "move_west": (0, -1),
        }

        dr, dc = deltas[action]
        r, c = self.agent_pos
        nr, nc = r + dr, c + dc
        target = self.grid[nr][nc]

        if target == "#":
            return StepResult(False, "Blocked by a wall.", self.done)

        if target == "D":
            return StepResult(False, "The door is locked.", self.done)

        self.agent_pos = (nr, nc)

        if target == "G":
            self.done = True
            return StepResult(True, "You reached the goal.", True, reward=1.0)

        return StepResult(True, f"Moved to {(nr, nc)}.", self.done)

    def _pick_up(self) -> StepResult:
        r, c = self.agent_pos

        # Check current cell or adjacent cells
        positions = [(r, c), (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

        for pr, pc in positions:
            if self.grid[pr][pc] == "K":
                self.grid[pr][pc] = "."
                if "key" not in self.inventory:
                    self.inventory.append("key")
                return StepResult(True, "Picked up the key.", self.done)

        return StepResult(False, "There is no key nearby.", self.done)

    def _unlock(self) -> StepResult:
        if "key" not in self.inventory:
            return StepResult(False, "You need a key to unlock the door.", self.done)

        r, c = self.agent_pos
        positions = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

        for pr, pc in positions:
            if self.grid[pr][pc] == "D":
                self.grid[pr][pc] = "."
                return StepResult(True, "Unlocked the door.", self.done)

        return StepResult(False, "There is no locked door nearby.", self.done)