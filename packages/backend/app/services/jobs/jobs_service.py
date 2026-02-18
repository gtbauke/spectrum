import logging

from typing import Callable
from uuid import UUID

from app.api.deps import UnitOfWork
from app.db.models.job import JobORM
from core.models.jobs.job import Job
from core.models.datasets.dataset import Dataset
from core.models.jobs.job_status import JobStatus

logger = logging.getLogger(__name__)


class JobsService:
    async def create(self, uow: UnitOfWork, *, dataset: Dataset) -> Job:
        async with uow:
            job = Job.new(dataset=dataset)

            orm = JobORM.from_domain(job)
            await uow.jobs.add(orm)

        return job

    async def get_by_id(self, uow: UnitOfWork, *, job_id: UUID) -> Job:
        async with uow:
            orm = await uow.jobs.get_by_id(job_id)

            if not orm:
                raise ValueError(f"Job with id {job_id} not found")

            domain = orm.to_domain()

        return domain

    async def update(
        self,
        uow: UnitOfWork,
        *,
        job_id: UUID,
        update_func: Callable[[JobORM], None],
    ) -> Job:
        async with uow:
            orm = await uow.jobs.get_for_update(job_id)

            if not orm:
                raise ValueError(f"Job with id {job_id} not found")

            update_func(orm)
            await uow.jobs.update(orm)

            domain = orm.to_domain()

        return domain

    async def update_status(self, uow: UnitOfWork, *, job_id: UUID, status: JobStatus) -> Job:
        async with uow:
            orm = await uow.jobs.get_for_update(job_id)

            if not orm:
                raise ValueError(f"Job with id {job_id} not found")

            orm.status = status
            domain = orm.to_domain()

        return domain

    async def list_all(self, uow: UnitOfWork, dataset_id: UUID) -> list[Job]:
        logger.info("GET jobs for dataset", extra={"dataset_id": dataset_id})

        async with uow:
            orms = await uow.jobs.list_all(where_id=dataset_id)
            return [orm.to_domain() for orm in orms]
