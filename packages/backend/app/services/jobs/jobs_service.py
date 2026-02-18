import logging

from typing import Callable
from uuid import UUID

from app.api.deps import UnitOfWork

from core.models.jobs.job import Job
from core.models.datasets.dataset import Dataset
from core.models.jobs.job_status import JobStatus

logger = logging.getLogger(__name__)


class JobsService:
    async def create(self, uow: UnitOfWork, *, dataset: Dataset) -> Job:
        async with uow:
            job = Job.new(dataset=dataset)
            await uow.jobs.add(job)

        return job

    async def get_by_id(self, uow: UnitOfWork, *, job_id: UUID) -> Job:
        async with uow:
            job = await uow.jobs.get_by_id(job_id)

            if not job:
                raise ValueError(f"Job with id {job_id} not found")

        return job

    async def update(
        self,
        uow: UnitOfWork,
        *,
        job_id: UUID,
        update_func: Callable[[Job], Job],
    ) -> Job:
        async with uow:
            job = await uow.jobs.get_for_update(job_id)

            if not job:
                raise ValueError(f"Job with id {job_id} not found")

            updated_job = update_func(job)
            await uow.jobs.update(updated_job)

        return updated_job

    async def update_status(self, uow: UnitOfWork, *, job_id: UUID, status: JobStatus) -> Job:
        async with uow:
            job = await uow.jobs.get_for_update(job_id)

            if not job:
                raise ValueError(f"Job with id {job_id} not found")

            updated_job = job.model_copy(
                update={
                    "status": status,
                }
            )

            await uow.jobs.update(updated_job)

        return updated_job

    async def list_all(self, uow: UnitOfWork, dataset_id: UUID) -> list[Job]:
        async with uow:
            jobs = await uow.jobs.list_all(dataset_id)
            return jobs
