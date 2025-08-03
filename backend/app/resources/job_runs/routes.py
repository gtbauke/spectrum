from sqlmodel import Session, select
from fastapi import APIRouter, Depends
from uuid import UUID
from app.resources.job_runs.models import JobRun, JobRunStatus
from app.database import get_session
from app.resources.job_runs.errors import JobRunNotFoundError

job_runs_router = APIRouter(prefix="/jobs/{job_id}/runs", tags=["job_runs"])


@job_runs_router.get("/")
def get_job_runs(job_id: UUID, session: Session = Depends(get_session)) -> list[JobRun]:
    """
    Retrieve all job runs for a specific job.
    """
    statement = select(JobRun).where(JobRun.job_id == job_id)
    job_runs = session.exec(statement).all()

    return list(job_runs)


@job_runs_router.get("/{run_id}")
def get_job_run(job_id: UUID, run_id: UUID, session: Session = Depends(get_session)) -> JobRun:
    """
    Retrieve a specific job run by its ID.
    """
    statement = select(JobRun).where(
        JobRun.job_id == job_id, JobRun.id == run_id)
    job_run = session.exec(statement).first()

    if job_run is None:
        raise JobRunNotFoundError(job_id=job_id, run_id=run_id)

    return job_run


@job_runs_router.post("/")
def create_job_run(job_id: UUID, session: Session = Depends(get_session)) -> JobRun:
    """
    Create a new job run for a specific job.
    """
    job_run = JobRun(job_id=job_id, status=JobRunStatus.PENDING)
    session.add(job_run)
    session.commit()
    session.refresh(job_run)

    return job_run
