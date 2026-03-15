from typing import Sequence

from app.features.profiles.versions.errors.profile_version_not_found import ProfileVersionNotFound
from core.models.jobs.job import Job
from core.models.jobs.job_version import JobVersion
from core.models.jobs.where import JobFilter, JobWhere
from core.models.profiles.where import ProfileVersionWhere
from core.ports.unit_of_work import UnitOfWork
from core.services.base import BaseImmutableVersionedService
from core.utils.filters.field_filter import UUIDFilter
from core.utils.pagination.base import Pagination

from .dto.create_job import CreateJob
from .dto.update_job import UpdateJob
from .errors.job_not_found import JobNotFound


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
        return await self.get_unique(
            uow=uow,
            where=where.model_copy(
                update={
                    "is_latest": True,
                }
            )
        )

    async def create(self, *, uow: UnitOfWork, data: CreateJob, version: int = 1) -> Job:
        new_job = Job.new(
            owner_id=data.owner_id,
            profile_version_id=data.profile_version_id,
        )

        if data.version:
            created_version = JobVersion.new(
                name=data.version.name,
                version=version,
                is_latest=True,
                job_id=new_job.id,
                dataset_artifact_id=data.version.dataset_artifact_id,
                generations=data.version.generations,
                population=data.version.population,
                max_size=data.version.max_size,
                number_of_tournaments=data.version.number_of_tournaments,
                crossover_probability=data.version.crossover_probability,
                mutation_probability=data.version.mutation_probability,
                non_terminals=data.version.non_terminals,
                loss=data.version.loss,
                optimization_iterations=data.version.optimization_iterations,
                optimization_repeats=data.version.optimization_repeats,
                max_param_count=data.version.max_param_count,
                split=data.version.split,
                simplify=data.version.simplify,
            )

            new_job.versions.append(created_version)

        job = await uow.jobs.add(new_job)
        return job

    async def create_new_version(self, *, uow: UnitOfWork, data: UpdateJob, where: JobWhere) -> Job:
        job = await uow.jobs.get_unique(
            where=where,
        )

        if not job:
            raise JobNotFound()

        if data.new_owner_id:
            job.owner_id = data.new_owner_id

        latest_job = job.versions[-1]
        if data.version:
            latest_job.is_latest = False
            update_job_version = data.version.to_create_job_data(
                latest_version=latest_job)

            job.versions.append(JobVersion.new(
                name=update_job_version.name,
                version=latest_job.version + 1,
                is_latest=True,
                job_id=job.id,
                dataset_artifact_id=update_job_version.dataset_artifact_id,
                generations=update_job_version.generations,
                population=update_job_version.population,
                max_size=update_job_version.max_size,
                number_of_tournaments=update_job_version.number_of_tournaments,
                crossover_probability=update_job_version.crossover_probability,
                mutation_probability=update_job_version.mutation_probability,
                non_terminals=update_job_version.non_terminals,
                loss=update_job_version.loss,
                optimization_iterations=update_job_version.optimization_iterations,
                optimization_repeats=update_job_version.optimization_repeats,
                max_param_count=update_job_version.max_param_count,
                split=update_job_version.split,
                simplify=update_job_version.simplify,
            ))

        updated_job = await uow.jobs.update(job)
        return updated_job

    async def get_all(self, *, uow: UnitOfWork, filter: JobFilter | None = None, pagination: Pagination | None = None) -> Sequence[Job]:
        return await uow.jobs.list_all(where=filter, pagination=pagination)

    async def get_paginated(self, *, uow: UnitOfWork, filter: JobFilter, limit: int = 20, offset: int = 0, for_profile: ProfileVersionWhere) -> tuple[list[Job], int]:
        latest_profile_version = await uow.profile_versions.get_unique(
            where=for_profile,
        )

        if not latest_profile_version:
            raise ProfileVersionNotFound()

        final_filter = JobFilter(
            AND=[
                filter,
                JobFilter(
                    profile_version_id=UUIDFilter(
                        eq=latest_profile_version.id),
                )
            ]
        )

        return await uow.jobs.get_paginated(filter=final_filter, limit=limit, offset=offset)


def get_jobs_service() -> JobsService:
    return JobsService()
