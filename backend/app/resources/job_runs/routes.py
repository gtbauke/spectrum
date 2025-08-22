from sqlmodel import Session
from fastapi import APIRouter, Depends, WebSocket
from uuid import UUID
from reggression import Reggression

from app.database import get_session
from app.utils.api_response import ApiResponse
from app.resources.job_runs.models import JobRun
from app.resources.job_runs.repository import get_all_job_runs, get_job_run_by_id, create_job_run
from app.tasks.create_sr_model import create_sr_model

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

    create_sr_model.delay(job_run.job.dataset.dataset_file_path,
                          str(job_run.id))

    return {"data": job_run}


@job_runs_router.websocket("/{run_id}/ws")
async def explore_job_run(
    websocket: WebSocket,
    run_id: UUID,
    session: Session = Depends(get_session)
):
    current_run = session.get(JobRun, run_id)
    if current_run is None or current_run.eggp_file_path is None:
        await websocket.close(code=1008)

    eggp = Regression(
        dataset=current_run.job.dataset.dataset_file_path,
        eggp_file_path=current_run.eggp_file_path
    )

    await websocket.accept()
    try:
        while True:
            # TODO: Implement the logic to handle WebSocket messages
            pass
    except Exception as e:
        await websocket.close(code=1011)
        raise e
