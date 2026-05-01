from core.types import StepResult


class ToolExecutor:
    def execute(self, tool_call, env) -> StepResult:
        name = tool_call["name"]
        args = tool_call.get("args", {})

        method = getattr(env, name, None)
        if method is None:
            return StepResult(False, f"Environment does not support tool: {name}", env.is_done())

        return method(**args)
