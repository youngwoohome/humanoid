from typing import Any, Dict, List, Type

class LLMClient:
    def __init__(self, model: str = "gpt-4o-mini"):
        self._load_env_file()

        from openai import OpenAI

        self.client = OpenAI(timeout=30.0, max_retries=1)
        self.model = model

    def _load_env_file(self) -> None:
        try:
            from dotenv import load_dotenv
        except ModuleNotFoundError:
            print("dotenv not found, skipping env file loading")
            return

        load_dotenv()

    def run_llm(self, messages: List[Dict[str, Any]], response_model: Type[Any]) -> Any:
        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=response_model,
        )
        parsed = response.choices[0].message.parsed
        return parsed
