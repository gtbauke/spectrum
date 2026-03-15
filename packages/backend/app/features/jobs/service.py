from typing import Sequence

from app.features.jobs.dto.create_job import CreateJob
from app.features.jobs.dto.update_job import UpdateJob
from app.features.jobs.errors.job_not_found import JobNotFound
from app.features.profiles.errors.profile_not_found import ProfileNotFound
from app.features.profiles.versions.errors.profile_version_not_found import ProfileVersionNotFound

from core.models.jobs.job import Job
from core.models.jobs.where import JobFilter, JobWhere
from core.models.profiles.where import ProfileVersionWhere
from core.ports.unit_of_work import UnitOfWork
from core.services.base import BaseImmutableVersionedService
from core.utils.pagination.base import Pagination


class JobsService(BaseImmutableVersionedService[
    Job,
    JobWhere,
    CreateJob,
    UpdateJob,
    JobFilter,
]):
    async def get_unique(self, *, uow: UnitOfWork, where: JobWhere) -> Job | None:
        return await uow.jobs.get_unique(where)

    async def get_latest(self, *, uow: UnitOfWork, where: JobWhere) -> Job | None:
        return await uow.jobs.get_unique(where=JobWhere(id=where.id, is_latest=True))

    async def create(self, *, uow: UnitOfWork, data: CreateJob, version: int = 1) -> Job:
        if not data.profile_id:
            raise ProfileNotFound()

        latest_profile_version = await uow.profile_versions.get_unique(
            where=ProfileVersionWhere(
                profile_id=data.profile_id,
                is_latest=True,
            )
        )

        if not latest_profile_version and not data.profile_version_id:
            raise ProfileVersionNotFound()

        profile_version_id = latest_profile_version.id \
            if latest_profile_version \
            else data.profile_version_id

        if not profile_version_id:
            raise ProfileVersionNotFound()

        return await uow.jobs.add(Job.new(
            name=data.name,
            profile_version_id=profile_version_id,
            dataset_artifact_id=data.dataset_artifact_id,
            generations=data.generations,
            population=data.population,
            max_size=data.max_size,
            number_of_tournaments=data.number_of_tournaments,
            crossover_probability=data.crossover_probability,
            mutation_probability=data.mutation_probability,
            non_terminals=data.non_terminals,
            loss=data.loss,
            optimization_iterations=data.optimization_iterations,
            optimization_repeats=data.optimization_repeats,
            max_param_count=data.max_param_count,
            split=data.split,
            simplify=data.simplify,
            version=version,
            is_latest=True,
        ))

    async def create_new_version(self, *, uow: UnitOfWork, data: UpdateJob, where: JobWhere) -> Job:
        last_version = await uow.jobs.unset_latest(where.model_copy(update={"is_latest": True}))
        next_version = 1 if not last_version else last_version.version + 1

        if not last_version:
            raise JobNotFound()

        new_data = data.to_create_job_data(last_version)
        return await self.create(uow=uow, data=new_data, version=next_version)

    async def get_all(self, *, uow: UnitOfWork, filter: JobFilter | None = None, pagination: Pagination | None = None) -> Sequence[Job]:
        return await uow.jobs.list_all(where=filter, pagination=pagination)

    async def get_paginated(self, *, uow: UnitOfWork, filter: JobFilter, limit: int = 20, offset: int = 0) -> tuple[list[Job], int]:
        return await uow.jobs.get_paginated(filter=filter, limit=limit, offset=offset)


def get_jobs_service() -> JobsService:
    return JobsService()
