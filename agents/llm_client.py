from typing import Any, Dict, List

class LLMClient:
    def __init__(self, model: str = "gpt-4o-mini"):
        self._load_env_file()

        from openai import OpenAI

        self.client = OpenAI()
        self.model = model

    def _load_env_file(self) -> None:
        try:
            from dotenv import load_dotenv
        except ModuleNotFoundError:
            print("dotenv not found, skipping env file loading")
            return

        load_dotenv()

    def complete_json(self, messages: List[Dict[str, Any]]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content or ""
