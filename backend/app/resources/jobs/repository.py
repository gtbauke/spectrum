from uuid import UUID
from sqlmodel import Session, select

from app.resources.datasets.models import Dataset
from app.resources.jobs.models import Job, CreateJob
from app.resources.jobs.errors import DatasetNotFoundError, JobNotFoundError, JobWithFileNameAlreadyExistsError
from app.utils.id import ID, cast_to_uuid


async def get_all_jobs(
    dataset_id: UUID,
    session: Session
):
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        raise DatasetNotFoundError(str(dataset_id))

    query = select(Job).where(Job.dataset_id == dataset_id)
    jobs = session.exec(query).all()

    return jobs


async def get_job_by_id(job_id: ID, session: Session):
    job = session.get(Job, job_id)
    if not job:
        raise JobNotFoundError(job_id)

    return job


async def exists_job_with_id(job_id: ID, session: Session):
    job = session.get(Job, job_id)
    return job is not None


async def exists_job_with_file_name(dataset_id: ID, file_name: str, session: Session):
    existing_job = session.exec(
        select(Job)
        .where(Job.dataset_id == dataset_id, Job.file_name == file_name)
    ).first()

    return existing_job is not None


async def create_job(dataset_id: ID, data: CreateJob, session: Session):
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        raise DatasetNotFoundError(dataset_id)

    if await exists_job_with_file_name(dataset_id, data.file_name, session):
        raise JobWithFileNameAlreadyExistsError(data.file_name)

    job = Job(
        description=data.description,
        file_name=data.file_name,
        dataset_id=cast_to_uuid(dataset_id),
        generations=data.generations,
        population_size=data.population_size,
        max_expression_size=data.max_expression_size,
        tournament_size=data.tournament_size,
        crossover_probability=data.crossover_probability,
        mutation_probability=data.mutation_probability,
        loss_function=data.loss_function,
        max_optimization_iterations=data.max_optimization_iterations,
        max_optimization_restarts=data.max_optimization_restarts,
        parameter_count=data.parameter_count,
        split=data.split,
        simplify=data.simplify,
    )

    session.add(job)
    session.commit()
    session.refresh(job)

    return job


async def create_default_job(dataset_id: ID, session: Session):
    default_description = f"Default job for dataset {dataset_id}"
    default_file_name = f"{dataset_id}.egraph"

    job = Job(
        description=default_description,
        file_name=default_file_name,
        dataset_id=cast_to_uuid(dataset_id),
    )

    session.add(job)
    session.commit()
    session.refresh(job)

    return job
