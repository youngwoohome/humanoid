from typing import Any, Dict

from core.types import ValidationResult


class ToolValidator:
    def validate(self, tool_call: Dict[str, Any], tool_registry, env) -> ValidationResult:
        name = tool_call.get("name")
        args = tool_call.get("args", {})

        if not name:
            return ValidationResult(False, "Tool call is missing a name.")

        if not tool_registry.has_tool(name):
            return ValidationResult(False, f"Unknown tool: {name}")

        if not isinstance(args, dict):
            return ValidationResult(False, "Tool args must be an object.")

        spec = tool_registry.get(name)
        for required_key in spec.to_dict()["required"]:
            if required_key not in args:
                return ValidationResult(False, f"Missing required argument: {required_key}")

        for arg_name, schema in spec.args_schema.items():
            if arg_name not in args:
                continue
            error = self._validate_arg(arg_name, args[arg_name], schema)
            if error:
                return ValidationResult(False, error)

        if hasattr(env, "can_execute_tool"):
            approved, reason = env.can_execute_tool(name, args)
            if not approved:
                return ValidationResult(False, reason)

        return ValidationResult(True, "Tool call approved.")

    def _validate_arg(self, name: str, value: Any, schema: Dict[str, Any]) -> str:
        if value is None and schema.get("nullable"):
            return ""

        expected_type = schema.get("type")
        if expected_type == "string" and not isinstance(value, str):
            return f"Argument '{name}' must be a string."

        if "enum" in schema and value not in schema["enum"]:
            return f"Argument '{name}' must be one of {schema['enum']}."

        return ""
