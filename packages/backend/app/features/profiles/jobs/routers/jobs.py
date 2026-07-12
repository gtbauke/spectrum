from uuid import UUID
from fastapi import APIRouter, Depends, status

from app.api.unit_of_work import get_uow
from app.features.profiles.jobs.errors.job_not_found import JobNotFound
from core.ports.unit_of_work import UnitOfWork

from app.features.auth.guards.get_current_user import get_current_user
from app.features.profiles.guards.can_edit_profile import can_edit_profile

from app.features.profiles.jobs.dtos.create import CreateJobDto
from app.features.profiles.jobs.dtos.update import UpdateJobDto, BulkUpdateJobDto

from core.features.profiles.jobs.job import Job
from core.features.profiles.jobs.where import JobWhere, JobFilter
from core.utils.filters.field_filter import UUIDFilter
from core.utils.pagination.response import PaginatedResponse

from app.features.profiles.jobs.runs.routers.runs import runs_router

jobs_router = APIRouter()

jobs_router.include_router(
    runs_router, prefix="/{job_id}/runs", tags=["Runs"]
)


# TODO: add validation for active_group_by_columns to ensure they exist in the dataset and are valid for grouping
@jobs_router.post(
    path="",
    response_model=list[Job],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(can_edit_profile)],
)
async def create_jobs(
    profile_id: UUID,
    dtos: list[CreateJobDto],
    uow: UnitOfWork = Depends(get_uow),
):
    jobs = [
        Job.new(
            profile_id=profile_id,
            name=dto.name,
            runs_against=dto.runs_against,
            generations=dto.generations,
            population=dto.population,
            max_size=dto.max_size,
            number_of_tournaments=dto.number_of_tournaments,
            crossover_probability=dto.crossover_probability,
            mutation_probability=dto.mutation_probability,
            non_terminals=dto.non_terminals,
            loss=dto.loss,
            optimization_iterations=dto.optimization_iterations,
            optimization_repeats=dto.optimization_repeats,
            max_param_count=dto.max_param_count,
            split=dto.split,
            simplify=dto.simplify,
            active_group_by_columns=dto.active_group_by_columns,
        ) for dto in dtos
    ]

    await uow.jobs.add_many(jobs)
    return jobs


@jobs_router.put(
    path="",
    response_model=list[Job],
    dependencies=[Depends(can_edit_profile)],
)
async def bulk_update_jobs(
    profile_id: UUID,
    dtos: list[BulkUpdateJobDto],
    uow: UnitOfWork = Depends(get_uow),
):
    jobs = []

    for dto in dtos:
        job = await uow.jobs.get_unique(JobWhere(id=dto.id))
        if not job or job.profile_id != profile_id:
            raise JobNotFound()

        update_data = dto.model_dump(exclude_unset=True, exclude={'id'})
        if update_data:
            job = job.model_copy(update=update_data)

        jobs.append(job)

    await uow.jobs.update_many(jobs)
    return jobs


@jobs_router.put(
    path="/{job_id}",
    response_model=Job,
    dependencies=[Depends(can_edit_profile)],
)
async def update_job(
    profile_id: UUID,
    job_id: UUID,
    dto: UpdateJobDto,
    uow: UnitOfWork = Depends(get_uow),
):
    job = await uow.jobs.get_unique(JobWhere(id=job_id))
    if not job or job.profile_id != profile_id:
        raise JobNotFound()

    update_data = dto.model_dump(exclude_unset=True)
    if update_data:
        job = job.model_copy(update=update_data)

    await uow.jobs.update(job)
    return job


@jobs_router.delete(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(can_edit_profile)],
)
async def bulk_delete_jobs(
    profile_id: UUID,
    job_ids: list[UUID],
    uow: UnitOfWork = Depends(get_uow),
):
    jobs = []
    for job_id in job_ids:
        job = await uow.jobs.get_unique(JobWhere(id=job_id))

        if not job or job.profile_id != profile_id:
            raise JobNotFound()

        jobs.append(job)

    await uow.jobs.delete_many(jobs)
    return None


@jobs_router.delete(
    path="/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(can_edit_profile)],
)
async def delete_job(
    profile_id: UUID,
    job_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
):
    job = await uow.jobs.get_unique(JobWhere(id=job_id))

    if not job or job.profile_id != profile_id:
        raise JobNotFound()

    await uow.jobs.delete(job)
    return None


@jobs_router.get(
    path="",
    response_model=PaginatedResponse[Job],
    dependencies=[Depends(get_current_user)],
)
async def list_jobs(
    profile_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
):
    job_filter = JobFilter(profile_id=UUIDFilter(eq=profile_id))
    jobs = await uow.jobs.list(filter=job_filter)
    return jobs


@jobs_router.get(
    path="/{job_id}",
    response_model=Job,
    dependencies=[Depends(get_current_user)],
)
async def get_job(
    profile_id: UUID,
    job_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
):
    job = await uow.jobs.get_unique(JobWhere(id=job_id))

    if not job or job.profile_id != profile_id:
        raise JobNotFound()

    return job
