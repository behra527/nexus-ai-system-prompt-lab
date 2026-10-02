from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    """Schema for validating structured LLM responses."""

    summary: str = Field(
        description="Short summary of the answer."
    )

    analysis: str = Field(
        description="Technical analysis."
    )

    recommendation: str = Field(
        description="Recommended approach."
    )

    risks: list[str] = Field(
        description="Potential risks or limitations."
    )

    confidence: str = Field(
        description="Confidence level: high, medium, or low."
    )