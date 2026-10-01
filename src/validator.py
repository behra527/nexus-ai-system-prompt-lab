import json

from pydantic import ValidationError

from .schemas import AIResponse


def validate_response(response: str) -> tuple[bool, str]:
    """
    Validate an LLM response against the expected
    AIResponse schema.
    """

    try:

        data = json.loads(response)

    except json.JSONDecodeError as exc:

        return (
            False,
            f"Invalid JSON: {exc.msg}",
        )

    if not isinstance(data, dict):

        return (
            False,
            "Invalid structure: expected a JSON object.",
        )

    try:

        validated = AIResponse.model_validate(data)

        return (
            True,
            validated.model_dump_json(indent=2),
        )

    except ValidationError as exc:

        errors = []

        for error in exc.errors():

            location = ".".join(
                str(item)
                for item in error["loc"]
            )

            errors.append(
                f"{location}: {error['msg']}"
            )

        return (
            False,
            "\n".join(errors),
        )