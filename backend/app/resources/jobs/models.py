from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from uuid import UUID, uuid4
from enum import Enum
from app.resources.datasets.models import Dataset


class LossFunction(str, Enum):
    MSE = "MSE"
    GAUSSIAN = "Gaussian"
    BERNOULLI = "Bernoulli"
    POISSON = "Poisson"


class CreateJob(SQLModel):
    description: str
    file_name: str
    dataset_id: UUID
    generations: int = 100
    population_size: int = 100
    max_expression_size: int = 15
    tournament_size: int = 3
    crossover_probability: float = 0.9
    mutation_probability: float = 0.3
    non_terminals: list[str] = ["add", "sub", "mul", "div"]
    loss_function: LossFunction = LossFunction.MSE
    max_optimization_iterations: int = 50
    max_optimization_restarts: int = 2
    parameter_count: int = -1
    split: int = 1
    simplify: bool = False


class Job(CreateJob, table=True):
    __tablename__: str = "jobs"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    description: str = Field(max_length=255)
    file_name: str = Field(max_length=255)

    dataset_id: UUID = Field(foreign_key="datasets.id")
    dataset: Dataset = Relationship(back_populates="jobs")

    generations: int = Field(default=100)
    population_size: int = Field(default=100)
    max_expression_size: int = Field(default=15)
    tournament_size: int = Field(default=3)
    crossover_probability: float = Field(default=0.9)
    mutation_probability: float = Field(default=0.3)
    non_terminals: list[str] = Field(default=["add", "sub", "mul", "div"])
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
