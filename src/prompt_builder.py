from prompts.system_prompts import build_system_prompt


def build_messages(
    user_prompt: str,
    role: str,
    tone: str,
    response_style: str,
    output_format: str,
    safety_level: str,
    accuracy_level: str,
) -> list[dict[str, str]]:
    """
    Build system and user messages for an LLM request.
    """

    system_prompt = build_system_prompt(
        role=role,
        tone=tone,
        response_style=response_style,
        output_format=output_format,
        safety_level=safety_level,
        accuracy_level=accuracy_level,
    )

    return [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt.strip(),
        },
    ]