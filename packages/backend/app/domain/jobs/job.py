from __future__ import annotations

from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from app.domain.jobs.job_status import JobStatus
from app.domain.jobs.loss_function import LossFunction
from app.domain.jobs.available_functions import AvailableFunctions

if TYPE_CHECKING:
    from app.domain.datasets.dataset import Dataset
    from app.domain.models.model import Model


class Job(BaseModel):
    id: UUID = Field(..., description="The unique identifier of the job")
    status: JobStatus = Field(
        JobStatus.PENDING, description="The current status of the job")
    dataset_id: UUID = Field(
        ..., description="The unique identifier of the dataset associated with the job")
    created_at: datetime = Field(...,
                                 description="The creation timestamp of the job")
    started_at: datetime | None = Field(
        None, description="The timestamp when the job started, if it has started"
    )
    finished_at: datetime | None = Field(
        None, description="The timestamp when the job finished, if it has finished"
    )

    model: Optional["Model"] = Field(None,
                                     description="The model produced by the job")

    generations: int = Field(...,
                             description="The number of generations for the genetic algorithm")
    population: int = Field(...,
                            description="The population size for the genetic algorithm")
    max_size: int = Field(...,
                          description="The maximum size of the expression")
    number_of_tournaments: int = Field(
        ..., description="The number of tournaments for the genetic algorithm")
    crossover_probability: float = Field(
        ..., description="The crossover probability for the genetic algorithm")
    mutation_probability: float = Field(
        ..., description="The mutation probability for the genetic algorithm")
    non_terminals: list[AvailableFunctions] = Field(
        ..., description="The non-terminals to be used in the genetic programming")
    loss: LossFunction = Field(
        ..., description="The loss function to be used for evaluating the models")
    optimization_iterations: int = Field(
        ..., description="The number of optimization iterations for the models")
    optimization_repeats: int = Field(
        ..., description="The number of optimization repeats for the models")
    max_param_count: int = Field(
        ..., description="The maximum number of parameters for the models")
    split: int = Field(...,
                       description="The split to be used for training and testing the models")
    simplify: bool = Field(...,
                           description="Whether to simplify the expressions of the models")

    @classmethod
    def new(cls, dataset: "Dataset") -> Job:
        return cls(
            id=uuid4(),
            status=JobStatus.PENDING,
            dataset_id=dataset.id,
            created_at=datetime.now(),
            started_at=None,
            finished_at=None,
            model=None,
            generations=100,
            population=100,
            max_size=15,
            number_of_tournaments=3,
            crossover_probability=0.9,
            mutation_probability=0.3,
            non_terminals=[
                AvailableFunctions.ADD,
                AvailableFunctions.SUB,
                AvailableFunctions.MUL,
                AvailableFunctions.DIV,
            ],
            loss=LossFunction.MSE,
            optimization_iterations=50,
            optimization_repeats=2,
            max_param_count=-1,
            split=1,
            simplify=False,
        )
