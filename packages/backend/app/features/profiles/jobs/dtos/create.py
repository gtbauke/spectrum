from uuid import UUID
from pydantic import BaseModel, Field

from core.features.profiles.jobs.available_function import AvailableFunction
from core.features.profiles.jobs.loss_function import LossFunction


class CreateJobDto(BaseModel):
    name: str = Field(..., description="The name of the job")
    runs_against: UUID = Field(..., description="The ID of the dataset it runs against")
    generations: int = Field(default=100, description="The number of generations for the genetic algorithm")
    population: int = Field(default=100, description="The population size for the genetic algorithm")
    max_size: int = Field(default=15, description="The maximum size of the expression")
    number_of_tournaments: int = Field(default=3, description="The number of tournaments for the genetic algorithm")
    crossover_probability: float = Field(default=0.9, description="The crossover probability for the genetic algorithm")
    mutation_probability: float = Field(default=0.3, description="The mutation probability for the genetic algorithm")
    non_terminals: list[AvailableFunction] = Field(
        default_factory=AvailableFunction.default,
        description="The non-terminals to be used in the genetic programming",
    )
    loss: LossFunction = Field(
        default=LossFunction.MSE,
        description="The loss function to be used for evaluating the models",
    )
    optimization_iterations: int = Field(default=50, description="The number of optimization iterations for the models")
    optimization_repeats: int = Field(default=2, description="The number of optimization repeats for the models")
    max_param_count: int = Field(default=-1, description="The maximum number of parameters (-1 means unlimited)")
    split: int = Field(default=1, description="The split to be used for training and testing the models")
    simplify: bool = Field(default=False, description="Whether to simplify the expressions of the models")
