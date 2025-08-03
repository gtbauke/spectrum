from sqlmodel import Session
from fastapi import APIRouter, Depends
from uuid import UUID

from app.database import get_session
from app.utils.api_response import ApiResponse
from app.resources.job_runs.models import JobRun
from app.resources.job_runs.repository import get_all_job_runs, get_job_run_by_id, create_job_run

job_runs_router = APIRouter(prefix="/jobs/{job_id}/runs", tags=["job_runs"])


@job_runs_router.get("/", response_model=ApiResponse[list[JobRun]])
async def get_job_runs(job_id: UUID, session: Session = Depends(get_session)):
    """
    Retrieve all job runs for a specific job.
    """
    job_runs = await get_all_job_runs(job_id, session)
    return {"data": job_runs}


@job_runs_router.get("/{run_id}", response_model=ApiResponse[JobRun])
async def get_job_run(job_id: UUID, run_id: UUID, session: Session = Depends(get_session)):
    """
    Retrieve a specific job run by its ID.
    """
    job_run = await get_job_run_by_id(job_id, run_id, session)
    return {"data": job_run}


@job_runs_router.post("/", status_code=201, response_model=ApiResponse[JobRun])
async def create_job_run_(job_id: UUID, session: Session = Depends(get_session)):
    """
    Create a new job run for a specific job.
    """
    job = await create_job_run(job_id, session)
    return {"data": job}
