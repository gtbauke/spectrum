from sqlmodel import Session, select

from app.utils.id import ID, cast_to_uuid
from app.resources.job_runs.models import JobRun, JobRunStatus
from app.resources.job_runs.errors import JobRunNotFoundError


async def get_all_job_runs(job_id: ID, session: Session):
    query = select(JobRun).where(JobRun.job_id == cast_to_uuid(job_id))
    result = session.exec(query).all()

    return result


async def get_job_run_by_id(job_id: ID, run_id: ID, session: Session) -> JobRun:
    query = select(JobRun).where(
        JobRun.job_id == cast_to_uuid(job_id),
        JobRun.id == cast_to_uuid(run_id)
    )

    job_run = session.exec(query).first()

    if job_run is None:
        raise JobRunNotFoundError(job_id=job_id, run_id=run_id)

    return job_run


async def create_job_run(job_id: ID, session: Session) -> JobRun:
    job_run = JobRun(job_id=cast_to_uuid(job_id), status=JobRunStatus.PENDING)
    session.add(job_run)
    session.commit()
    session.refresh(job_run)

    return job_run
