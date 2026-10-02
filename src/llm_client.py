import os

from dotenv import load_dotenv
from openai import (
    OpenAI,
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    RateLimitError,
)


load_dotenv()


def get_client() -> OpenAI:
    """Create an OpenRouter client using an environment variable."""

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is missing. "
            "Add it to the .env file."
        )

    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


def generate_response(
    messages: list[dict[str, str]],
    model: str,
) -> str:
    """Generate an LLM response using OpenRouter."""

    client = get_client()

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
            max_tokens=2048,
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError(
                "The LLM returned an empty response."
            )

        return content

    except AuthenticationError:
        raise RuntimeError(
            "Authentication failed. Please check your API key."
        )

    except RateLimitError:
        raise RuntimeError(
            "Rate limit reached. Please wait and try again."
        )

    except APIConnectionError:
        raise RuntimeError(
            "Could not connect to the LLM API."
        )

    except APIStatusError as error:

        if error.status_code == 402:
            raise RuntimeError(
                "Insufficient OpenRouter credits or token limit."
            )

        raise RuntimeError(
            f"LLM API error: {error.status_code}"
        )