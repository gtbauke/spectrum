from db.common.mappers.base import IMapper
from db.features.profiles.jobs.model import JobORM

from core.features.profiles.jobs.job import Job
from core.features.profiles.jobs.available_function import AvailableFunction
from core.features.profiles.jobs.loss_function import LossFunction

from .runs.mapper import RunsMapper


class JobsMapper(IMapper[JobORM, Job]):
    @staticmethod
    def to_domain(orm: JobORM) -> Job:
        return Job(
            id=orm.id,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            name=orm.name,
            profile_id=orm.profile_id,
            runs_against=orm.runs_against,
            generations=orm.generations,
            population=orm.population,
            max_size=orm.max_size,
            number_of_tournaments=orm.number_of_tournaments,
            crossover_probability=orm.crossover_probability,
            mutation_probability=orm.mutation_probability,
            non_terminals=AvailableFunction.to_list(orm.non_terminals),
            loss=LossFunction(orm.loss),
            optimization_iterations=orm.optimization_iterations,
            optimization_repeats=orm.optimization_repeats,
            max_param_count=orm.max_param_count,
            split=orm.split,
            simplify=orm.simplify,
            runs=[
                RunsMapper.to_domain(run)
                for run in orm.runs
            ],
            active_group_by_columns=orm.active_group_by_columns.split(
                ",") if orm.active_group_by_columns else None,
        )

    @staticmethod
    def to_orm(domain: Job) -> JobORM:
        return JobORM(
            id=domain.id,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            name=domain.name,
            profile_id=domain.profile_id,
            runs_against=domain.runs_against,
            generations=domain.generations,
            population=domain.population,
            max_size=domain.max_size,
            number_of_tournaments=domain.number_of_tournaments,
            crossover_probability=domain.crossover_probability,
            mutation_probability=domain.mutation_probability,
            non_terminals=AvailableFunction.from_list(*domain.non_terminals),
            loss=domain.loss.value,
            optimization_iterations=domain.optimization_iterations,
            optimization_repeats=domain.optimization_repeats,
            max_param_count=domain.max_param_count,
            split=domain.split,
            simplify=domain.simplify,
            runs=[
                RunsMapper.to_orm(run)
                for run in domain.runs
            ],
            active_group_by_columns=",".join(
                domain.active_group_by_columns) if domain.active_group_by_columns else None,
        )
