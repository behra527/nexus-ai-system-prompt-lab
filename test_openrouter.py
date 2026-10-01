import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

print("Key loaded:", bool(api_key))
print("Key length:", len(api_key) if api_key else 0)
print("Key prefix:", api_key[:10] if api_key else None)


client = OpenAI(
    api_key=api_key.strip(),
    base_url="https://openrouter.ai/api/v1",
)


response = client.chat.completions.create(
    model="x-ai/grok-4.3",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a concise technical AI assistant."
            ),
        },
        {
            "role": "user",
            "content": (
                "Explain what a system prompt is in one sentence."
            ),
        },
    ],
    temperature=0.2,
    max_tokens=500,
)


print("\n--- MODEL RESPONSE ---")

print(response.choices[0].message.content)

print("\n--- USAGE ---")

if response.usage:
    print("Prompt tokens:", response.usage.prompt_tokens)
    print("Completion tokens:", response.usage.completion_tokens)
    print("Total tokens:", response.usage.total_tokens)