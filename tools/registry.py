from typing import Dict, List

from tools.base import ToolSpec


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, ToolSpec] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        for spec in [
            ToolSpec("look", "Observe the current environment.", required=[]),
            ToolSpec(
                "move",
                "Move the agent one step in a direction.",
                {"direction": {"type": "string", "enum": ["north", "south", "east", "west", "forward"]}},
            ),
            ToolSpec(
                "scan",
                "Search the current observation for objects or exits.",
                {"query": {"type": "string", "nullable": True}},
                required=[],
            ),
            ToolSpec(
                "pick_up",
                "Pick up an item from the current location or nearby area.",
                {"item": {"type": "string", "enum": ["key"]}},
            ),
            ToolSpec(
                "unlock",
                "Unlock a target using an item.",
                {
                    "target": {"type": "string", "enum": ["door"]},
                    "using": {"type": "string", "enum": ["key"]},
                },
            ),
            ToolSpec(
                "interact",
                "Interact with a target object.",
                {"target": {"type": "string"}},
            ),
        ]:
            self.register(spec)

    def register(self, spec: ToolSpec) -> None:
        self._tools[spec.name] = spec

    def specs(self) -> List[dict]:
        return [spec.to_dict() for spec in self._tools.values()]

    def get(self, name: str) -> ToolSpec:
        return self._tools[name]

    def has_tool(self, name: str) -> bool:
        return name in self._tools
