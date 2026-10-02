from pydantic import ValidationError

from src.schemas import LLMResponse


def validate_llm_response(
    response: str,
) -> tuple[bool, LLMResponse | None, str | None]:
    """
    Validate an LLM response against the LLMResponse schema.
    """

    try:
        parsed_response = LLMResponse.model_validate_json(response)

        return True, parsed_response, None

    except ValidationError as error:
        return False, None, str(error)

    except Exception as error:
        return False, None, str(error)