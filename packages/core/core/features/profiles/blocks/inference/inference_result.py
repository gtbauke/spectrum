from uuid import UUID
from pydantic import Field
from typing import Optional
from core.features.base import BaseImmutableDomainModel


class InferenceResult(BaseImmutableDomainModel):
    """
    Represents a single result (expression) from an IQL execution run.
    """
    run_id: UUID = Field(...,
                         description="The ID of the run this result belongs to")
    run_version: int = Field(...,
                             description="The version of the run this result belongs to")

    expression: str = Field(..., description="The mathematical expression")
    dl: Optional[float] = Field(None, description="DL score of the expression")
    fitness: Optional[float] = Field(
        None, description="Fitness score of the expression")
    latex: Optional[str] = Field(None, description="LaTeX representation")
    numpy: Optional[str] = Field(None, description="NumPy representation")
    parameters: Optional[dict[str, float]] = Field(
        None, description="Parameters found")
    size: Optional[int] = Field(None, description="Size of the expression")
    frequency: Optional[int] = Field(
        None, description="Frequency of the pattern/expression")
    prediction: Optional[list[float]] = Field(
        None, description="Prediction output array")
    egraph_id: Optional[str] = Field(
        None, description="The internal egraph ID referencing this expression")

    @classmethod
    def new(
        cls,
        run_id: UUID,
        run_version: int,
        expression: str,
        dl: Optional[float] = None,
        fitness: Optional[float] = None,
        latex: Optional[str] = None,
        numpy: Optional[str] = None,
        parameters: Optional[dict[str, float]] = None,
        size: Optional[int] = None,
        frequency: Optional[int] = None,
        prediction: Optional[list[float]] = None,
        egraph_id: Optional[str] = None,
    ):
        return cls(
            run_id=run_id,
            run_version=run_version,
            expression=expression,
            dl=dl,
            fitness=fitness,
            latex=latex,
            numpy=numpy,
            parameters=parameters,
            size=size,
            frequency=frequency,
            prediction=prediction,
            egraph_id=egraph_id,
        )
