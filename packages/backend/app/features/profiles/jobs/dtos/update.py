from uuid import UUID
from pydantic import BaseModel, Field

from core.features.profiles.jobs.available_function import AvailableFunction
from core.features.profiles.jobs.loss_function import LossFunction


class UpdateJobDto(BaseModel):
    name: str | None = Field(None, description="The name of the job")
    runs_against: UUID | None = Field(
        None, description="The ID of the dataset it runs against")
    generations: int | None = Field(
        None, description="The number of generations for the genetic algorithm")
    population: int | None = Field(
        None, description="The population size for the genetic algorithm")
    max_size: int | None = Field(
        None, description="The maximum size of the expression")
    number_of_tournaments: int | None = Field(
        None, description="The number of tournaments for the genetic algorithm")
    crossover_probability: float | None = Field(
        None, description="The crossover probability for the genetic algorithm")
    mutation_probability: float | None = Field(
        None, description="The mutation probability for the genetic algorithm")
    non_terminals: list[AvailableFunction] | None = Field(
        None, description="The non-terminals to be used in the genetic programming")
    loss: LossFunction | None = Field(
        None, description="The loss function to be used for evaluating the models")
    optimization_iterations: int | None = Field(
        None, description="The number of optimization iterations for the models")
    optimization_repeats: int | None = Field(
        None, description="The number of optimization repeats for the models")
    max_param_count: int | None = Field(
        None, description="The maximum number of parameters for the models")
    split: int | None = Field(
        None, description="The split to be used for training and testing the models")
    simplify: bool | None = Field(
        None, description="Whether to simplify the expressions of the models")


class BulkUpdateJobDto(UpdateJobDto):
    id: UUID = Field(..., description="The ID of the job to update")
