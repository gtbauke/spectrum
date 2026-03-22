from uuid import UUID
from pydantic import BaseModel, Field

from core.features.profiles.jobs.available_function import AvailableFunction
from core.features.profiles.jobs.loss_function import LossFunction


class CreateJobDto(BaseModel):
    name: str = Field(..., description="The name of the job")
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
