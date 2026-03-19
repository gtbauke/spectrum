from typing import Sequence

from app.features.job_runs.dto.create_job_run import CreateJobRun
from app.features.job_runs.dto.update_job_run import UpdateJobRun
from app.features.job_runs.errors.job_run_not_found import JobRunNotFound
from core.models.job_runs.job_run import JobRun
from core.models.job_runs.job_run_status import JobRunStatus
from core.models.job_runs.where import JobRunFilter, JobRunWhere
from core.ports.unit_of_work import UnitOfWork
from core.services.base import BaseCRUDService


class JobRunsService(BaseCRUDService[
    JobRun,
    JobRunWhere,
    CreateJobRun,
    UpdateJobRun,
    JobRunFilter,
]):
    async def get_unique(self, *, uow: UnitOfWork, where: JobRunWhere) -> JobRun | None:
        return await uow.job_runs.get_unique(where=where)

    async def create(self, *, uow: UnitOfWork, data: CreateJobRun) -> JobRun:
        run = JobRun.new(job_id=data.job_id)
        return await uow.job_runs.add(run)

    async def update_unique(self, *, uow: UnitOfWork, where: JobRunWhere, data: UpdateJobRun) -> JobRun:
        run = await uow.job_runs.get_for_update(where=where)

        if not run:
            raise JobRunNotFound(job_run_id=where.id)

        updated_run = run.model_copy(
            update=data.model_dump(exclude_unset=True))

        return await uow.job_runs.update(updated_run)

    async def delete_unique(self, *, uow: UnitOfWork, where: JobRunWhere):
        run = await uow.job_runs.get_for_update(where=where)

        if not run:
            raise JobRunNotFound(job_run_id=where.id)

        updated_run = run.model_copy(
            update={
                "job_run_status": JobRunStatus.DELETED,
            }
        )

        await uow.job_runs.update(updated_run)

    async def get_all(self, *, uow: UnitOfWork, filter: JobRunFilter | None = None) -> Sequence[JobRun]:
        return await uow.job_runs.list_all(where=filter)


def get_job_runs_service() -> JobRunsService:
    return JobRunsService()
