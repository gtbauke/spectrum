from uuid import UUID
from typing import Optional
from pydantic import BaseModel

from app.features.jobs.models import AvailableFunction
from core.models.jobs.job import Job
from core.models.jobs.loss_function import LossFunction

from .create_job import CreateJob


class UpdateJob(BaseModel):
    name: Optional[str] = None
    dataset_artifact_id: Optional[UUID] = None
    generations: Optional[int] = 100
    population: Optional[int] = 100
    max_size: Optional[int] = 15
    number_of_tournaments: Optional[int] = 3
    crossover_probability: Optional[float] = 0.9
    mutation_probability: Optional[float] = 0.3
    non_terminals: Optional[list[AvailableFunction]
                            ] = AvailableFunction.default()
    loss: Optional[LossFunction] = LossFunction.MSE
    optimization_iterations: Optional[int] = 50
    optimization_repeats: Optional[int] = 2
    max_param_count: Optional[int] = -1
    split: Optional[int] = 1
    simplify: Optional[bool] = False

    def to_create_job_data(self, latest_version: Job) -> CreateJob:
        name = latest_version.name if self.name is None else self.name
        dataset_artifact_id = latest_version.dataset_artifact_id if self.dataset_artifact_id is None else self.dataset_artifact_id
        generations = latest_version.generations if self.generations is None else self.generations
        population = latest_version.population if self.population is None else self.population
        max_size = latest_version.max_size if self.max_size is None else self.max_size
        number_of_tournaments = latest_version.number_of_tournaments if self.number_of_tournaments is None else self.number_of_tournaments
        crossover_probability = latest_version.crossover_probability if self.crossover_probability is None else self.crossover_probability
        mutation_probability = latest_version.mutation_probability if self.mutation_probability is None else self.mutation_probability
        non_terminals = latest_version.non_terminals if self.non_terminals is None else self.non_terminals
        loss = latest_version.loss if self.loss is None else self.loss
        optimization_iterations = latest_version.optimization_iterations if self.optimization_iterations is None else self.optimization_iterations
        optimization_repeats = latest_version.optimization_repeats if self.optimization_repeats is None else self.optimization_repeats
        max_param_count = latest_version.max_param_count if self.max_param_count is None else self.max_param_count
        split = latest_version.split if self.split is None else self.split
        simplify = latest_version.simplify if self.simplify is None else self.simplify

        return CreateJob(
            name=name,
            dataset_artifact_id=dataset_artifact_id,
            profile_id=None,
            profile_version_id=latest_version.profile_version_id,
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
        )
