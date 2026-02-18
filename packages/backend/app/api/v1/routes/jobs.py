from uuid import UUID
from fastapi import APIRouter, Depends
from app.services import get_jobs_service, JobsService
from app.api.deps import UnitOfWork, get_uow
from core.models.jobs.job import Job


jobs_router = APIRouter(tags=["jobs"])


@jobs_router.get("/", response_model=list[Job])
async def list_jobs(
    dataset_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    jobs_service: JobsService = Depends(get_jobs_service)
):
    async with uow:
        jobs = await jobs_service.list_all(uow=uow, dataset_id=dataset_id)

    return jobs


@jobs_router.get("/{job_id}", response_model=Job)
async def get_job(
    job_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    jobs_service: JobsService = Depends(get_jobs_service)
):
    async with uow:
        job = await jobs_service.get_by_id(uow=uow, job_id=job_id)

    return job
