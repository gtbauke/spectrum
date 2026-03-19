from uuid import UUID
from fastapi import APIRouter, Depends, status

from core.models.job_runs.job_run import JobRun
from core.ports.unit_of_work import UnitOfWork

from app.api.unit_of_work import get_uow
from app.features.job_runs.dto.create_job_run import CreateJobRun

from .service import JobRunsService, get_job_runs_service


job_runs_router = APIRouter(
    tags=["job_runs"],
)


@job_runs_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=JobRun,
)
async def create_job_run(
    job_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    service: JobRunsService = Depends(get_job_runs_service),
):
    return await service.create(uow=uow, data=CreateJobRun(job_id=job_id))
