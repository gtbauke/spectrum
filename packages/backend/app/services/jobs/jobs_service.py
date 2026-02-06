from uuid import UUID

from app.api.deps import UnitOfWork
from app.db.models.job import JobORM
from app.domain.jobs.job import Job
from app.domain.datasets.dataset import Dataset
from app.domain.jobs.job_status import JobStatus


class JobsService:
    async def create(self, uow: UnitOfWork, *, dataset: Dataset) -> Job:
        async with uow:
            job = Job.new(dataset=dataset)
            await uow.jobs.add(JobORM.from_domain(job))

        return job

    async def update_status(self, uow: UnitOfWork, *, job_id: UUID, status: JobStatus) -> Job:
        async with uow:
            orm = await uow.jobs.get_for_update(job_id)

            if not orm:
                raise ValueError(f"Job with id {job_id} not found")

            orm.status = status
            domain = orm.to_domain()

        return domain
