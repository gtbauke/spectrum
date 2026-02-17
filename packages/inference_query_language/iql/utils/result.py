import json
from pydantic import BaseModel, Field, field_validator
from typing import Any, Optional


class InferenceResult(BaseModel):
    id: Optional[int] = Field(None,
                              description="Unique identifier for the inference result")
    expression: Optional[str] = Field(None,
                                      description="The mathematical expression that was evaluated")
    dl: Optional[float] = Field(None, description="DL score of the expression")
    fitness: Optional[float] = Field(None,
                                     description="Fitness score of the expression")
    latex: Optional[str] = Field(None,
                                 description="LaTeX representation of the expression")
    numpy: Optional[str] = Field(None,
                                 description="NumPy code representation of the expression")
    parameters: Optional[list[float]] = Field(None,
                                              description="Parameters used in the expression")
    size: Optional[int] = Field(None,
                                description="Size of the expression (number of nodes in the AST)")

    model_config = {
        "extra": "allow",
    }

    @field_validator("parameters", mode="before")
    @classmethod
    def parse_parameters(cls, value: Optional[str]) -> Optional[list[float]]:
        if value is None:
            return None

        try:
            parsed: Any = json.loads(value)
            if isinstance(parsed, list):
                final: list[float] = []

                for item in parsed:  # type: ignore
                    if not isinstance(item, float):
                        try:
                            item = float(item)  # type: ignore
                        except ValueError:
                            raise ValueError(
                                "All items in the parameters list must be numbers")

                    final.append(item)

                return final
        except Exception:
            pass

        raise ValueError(
            "Parameters must be a JSON string representing a list of numbers")


class InferenceResultList(BaseModel):
    results: list[InferenceResult] = Field(...,
                                           description="List of inference results")
