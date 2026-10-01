from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AIResponse(BaseModel):
    """
    Expected structured response from the LLM.
    """

    model_config = ConfigDict(extra="forbid")

    summary: str = Field(
        min_length=1,
        description="Short summary of the answer.",
    )

    analysis: str = Field(
        min_length=1,
        description="Technical analysis of the answer.",
    )

    recommendation: str = Field(
        min_length=1,
        description="Recommended approach.",
    )

    risks: list[str] = Field(
        description="Potential risks or limitations.",
    )

    confidence: Literal[
        "high",
        "medium",
        "low",
    ]