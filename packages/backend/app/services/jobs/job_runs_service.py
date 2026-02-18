from uuid import UUID

from app.api.deps import UnitOfWork
from core.models.jobs.job_run import JobRun


class JobRunsService:
    async def get_runs_for_model(self, *, uow: UnitOfWork, model_id: UUID) -> list[JobRun]:
        job_runs = await uow.job_runs.list_all(where_id=model_id)
        return job_runs
