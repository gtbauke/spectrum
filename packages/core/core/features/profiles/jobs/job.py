from uuid import UUID
from pydantic import Field

from core.features.base import BaseMutableDomainModel

from .available_function import AvailableFunction
from .loss_function import LossFunction
from .runs.run import Run


class Job(BaseMutableDomainModel):
    name: str = Field(..., description="The name of the job")

    profile_id: UUID = Field(..., description="The ID of the profile")

    runs_against: UUID = Field(...,
                               description="The ID of the dataset it runs against")

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

    runs: list[Run] = Field([], description="The runs of the job")

    active_group_by_columns: list[str] | None = Field(
        None, description="The active group by columns for the job")

    @classmethod
    def new(
        cls,
        name: str,
        profile_id: UUID,
        runs_against: UUID,
        generations: int,
        population: int,
        max_size: int,
        number_of_tournaments: int,
        crossover_probability: float,
        mutation_probability: float,
        non_terminals: list[AvailableFunction],
        loss: LossFunction,
        optimization_iterations: int,
        optimization_repeats: int,
        max_param_count: int,
        split: int,
        simplify: bool,
        active_group_by_columns: list[str] | None = None,
    ) -> "Job":
        return cls(
            name=name,
            profile_id=profile_id,
            runs_against=runs_against,
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
            runs=[],
            active_group_by_columns=active_group_by_columns,
        )
