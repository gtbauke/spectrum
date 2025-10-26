from typing import Sequence
from sqlmodel import Session
from fastapi import APIRouter, Depends
from uuid import UUID

from app.database import get_session
from app.resources.job_runs.errors import JobRunNotFoundError
from app.utils.api_response import ApiResponse
from app.resources.job_runs.models import JobRun, JobRunQuery
from app.resources.job_runs.repository import get_all_job_runs, get_job_run_by_id, create_job_run
from app.tasks.create_sr_model import create_sr_model_task

job_runs_router = APIRouter(prefix="/jobs/{job_id}/runs", tags=["job_runs"])


@job_runs_router.get("/", response_model=ApiResponse[list[JobRun]])
async def get_job_runs(job_id: UUID, session: Session = Depends(get_session)) -> dict[str, Sequence[JobRun]]:
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
async def create_job_run_(
    job_id: UUID,
    session: Session = Depends(get_session),
):
    """
    Create a new job run for a specific job.
    """
    job_run = await create_job_run(job_id, session)

    if job_run.job.dataset.dataset_file_path is None:
        raise ValueError("Dataset file path is not set for the job's dataset.")

    create_sr_model_task.delay(job_run.job.dataset.dataset_file_path,
                               str(job_run.id))

    return {"data": job_run}


@job_runs_router.post("/{run_id}/model", status_code=200)
async def process_model_query(
    job_id: UUID,
    run_id: UUID,
    query: JobRunQuery,
    session: Session = Depends(get_session)
):
    """
    Process a query for the trained model
    """
    job_run = session.get(JobRun, run_id)
    if not job_run:
        raise JobRunNotFoundError(job_id, run_id)

    print(query.query)
    return {"data": query}
