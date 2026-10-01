import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class OpenRouterClient:
    """Client for interacting with LLMs through OpenRouter."""

    def __init__(self) -> None:
        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY is missing from .env"
            )

        self.client = OpenAI(
            api_key=api_key.strip(),
            base_url="https://openrouter.ai/api/v1",
        )

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "x-ai/grok-4.3",
        temperature: float = 0.2,
        max_tokens: int = 1000,
    ) -> dict:

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return {
            "content": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
        }