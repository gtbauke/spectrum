from pydantic import BaseModel, Field
from typing import Dict, List


class PredictRequestDto(BaseModel):
    expression_id: str | None = Field(
        None, description="Optional ID of the expression. If not provided, the best expression is used.")
    inputs: List[Dict[str, float]] = Field(
        ..., description="A list of objects containing variable and parameter mappings.")


class PredictResponseDto(BaseModel):
    expression_id: str = Field(..., description="ID of the expression used.")
    predictions: List[float] = Field(
        ..., description="The predicted values corresponding to the inputs.")
