from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from uuid import UUID, uuid4
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.resources.datasets.models import Dataset
    from app.resources.job_runs.models import JobRun


class LossFunction(str, Enum):
    MSE = "MSE"
    GAUSSIAN = "Gaussian"
    BERNOULLI = "Bernoulli"
    POISSON = "Poisson"


# TODO: Create non terminals in some sort of way
class CreateJob(SQLModel):
    description: str
    file_name: str
    generations: int = 100
    population_size: int = 100
    max_expression_size: int = 15
    tournament_size: int = 3
    crossover_probability: float = 0.9
    mutation_probability: float = 0.3
    loss_function: LossFunction = LossFunction.MSE
    max_optimization_iterations: int = 50
    max_optimization_restarts: int = 2
    parameter_count: int = -1
    split: int = 1
    simplify: bool = False


class UpdateJob(SQLModel):
    description: str | None = None
    file_name: str | None = None
    generations: int | None = None
    population_size: int | None = None
    max_expression_size: int | None = None
    tournament_size: int | None = None
    crossover_probability: float | None = None
    mutation_probability: float | None = None
    loss_function: LossFunction | None = None
    max_optimization_iterations: int | None = None
    max_optimization_restarts: int | None = None
    parameter_count: int | None = None
    split: int | None = None
    simplify: bool | None = None


class Job(CreateJob, table=True):
    __tablename__: str = "jobs"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    description: str = Field(max_length=255)
    file_name: str = Field(max_length=255)

    dataset_id: UUID = Field(foreign_key="datasets.id")
    dataset: "Dataset" = Relationship(back_populates="jobs")

    generations: int = Field(default=100)
    population_size: int = Field(default=100)
    max_expression_size: int = Field(default=15)
    tournament_size: int = Field(default=3)
    crossover_probability: float = Field(default=0.9)
    mutation_probability: float = Field(default=0.3)
    loss_function: LossFunction = Field(default=LossFunction.MSE)
    max_optimization_iterations: int = Field(default=50)
    max_optimization_restarts: int = Field(default=2)
    parameter_count: int = Field(default=-1)
    split: int = Field(default=1)
    simplify: bool = Field(default=False)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))

    runs: list["JobRun"] = Relationship(back_populates="job", sa_relationship_kwargs={
                                        "cascade": "all, delete-orphan"})
