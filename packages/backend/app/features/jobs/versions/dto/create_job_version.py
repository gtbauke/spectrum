from uuid import UUID

from pydantic import BaseModel

from app.features.jobs.models import AvailableFunction
from core.models.jobs.loss_function import LossFunction


class CreateJobVersion(BaseModel):
    name: str
    dataset_artifact_id: UUID
    generations: int = 100
    population: int = 100
    max_size: int = 15
    number_of_tournaments: int = 3
    crossover_probability: float = 0.9
    mutation_probability: float = 0.3
    non_terminals: list[AvailableFunction] = AvailableFunction.default()
    loss: LossFunction = LossFunction.MSE
    optimization_iterations: int = 50
    optimization_repeats: int = 2
    max_param_count: int = -1
    split: int = 1
    simplify: bool = False
