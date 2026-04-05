from uuid import UUID
from pydantic import Field
from typing import Optional
from core.features.base import BaseImmutableDomainModel


class InferenceResult(BaseImmutableDomainModel):
    """
    Represents a single result (expression) from an IQL execution run.
    """
    run_id: UUID = Field(..., description="The ID of the run this result belongs to")
    
    expression: str = Field(..., description="The mathematical expression")
    dl: Optional[float] = Field(None, description="DL score of the expression")
    fitness: Optional[float] = Field(None, description="Fitness score of the expression")
    latex: Optional[str] = Field(None, description="LaTeX representation")
    numpy: Optional[str] = Field(None, description="NumPy representation")
    parameters: Optional[dict[str, float]] = Field(None, description="Parameters found")
    size: Optional[int] = Field(None, description="Size of the expression")

    @classmethod
    def new(
        cls,
        run_id: UUID,
        expression: str,
        dl: Optional[float] = None,
        fitness: Optional[float] = None,
        latex: Optional[str] = None,
        numpy: Optional[str] = None,
        parameters: Optional[dict[str, float]] = None,
        size: Optional[int] = None
    ):
        return cls(
            run_id=run_id,
            expression=expression,
            dl=dl,
            fitness=fitness,
            latex=latex,
            numpy=numpy,
            parameters=parameters,
            size=size
        )
