from __future__ import annotations

from uuid import UUID
from pydantic import Field

from core.models.base import BaseImmutableVersionedDomainModel
from core.models.jobs.available_functions import AvailableFunction
from core.models.jobs.loss_function import LossFunction


class JobVersion(BaseImmutableVersionedDomainModel):
    job_id: UUID = Field(..., description="ID of the job")

    name: str = Field(default="Default Job",
                      description="Name of the job definition")

    dataset_artifact_id: UUID = Field(
        ..., description="ID of the artifact the job is running against")

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

    non_terminals: list[AvailableFunction] = Field(
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
    def new(
        cls,
        *,
        name: str,
        job_id: UUID,
        dataset_artifact_id: UUID,
        generations: int = 100,
        population: int = 100,
        max_size: int = 15,
        number_of_tournaments: int = 3,
        crossover_probability: float = 0.9,
        mutation_probability: float = 0.3,
        non_terminals: list[AvailableFunction] = [
            AvailableFunction.ADD,
            AvailableFunction.SUB,
            AvailableFunction.MUL,
            AvailableFunction.DIV,
        ],
        loss: LossFunction = LossFunction.MSE,
        optimization_iterations: int = 50,
        optimization_repeats: int = 2,
        max_param_count: int = -1,
        split: int = 1,
        simplify: bool = False,
        version: int = 1,
        is_latest: bool = True,
    ) -> JobVersion:
        return cls(
            name=name,
            job_id=job_id,
            dataset_artifact_id=dataset_artifact_id,
            generations=generations,
            population=population,
            max_size=max_size,
            number_of_tournaments=number_of_tournaments,
            crossover_probability=crossover_probability,
            mutation_probability=mutation_probability,
            non_terminals=non_terminals,
            loss=loss,
            optimization_iterations=optimization_iterations,
            optimization_repeats=optimization_repeats,
            max_param_count=max_param_count,
            split=split,
            simplify=simplify,
            version=version,
            is_latest=is_latest,
        )
