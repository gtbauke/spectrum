from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from uuid import UUID

from app.database import get_session
from app.resources.jobs.models import Job, CreateJob, UpdateJob
from app.resources.datasets.models import Dataset
from app.resources.jobs.errors import DatasetNotFoundError, JobWithFileNameAlreadyExistsError
from app.utils.api_response import ApiResponse

from app.resources.jobs.repository import get_all_jobs

job_router = APIRouter(prefix="/datasets/{dataset_id}/jobs", tags=["jobs"])


@job_router.get("/", response_model=ApiResponse[list[Job]])
async def get_jobs(dataset_id: UUID, session: Session = Depends(get_session)):
    jobs = await get_all_jobs(dataset_id, session)
    return {"data": jobs}


@job_router.post("/")
async def create_job(data: CreateJob, dataset_id: UUID, session: Session = Depends(get_session)) -> Job:
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        raise DatasetNotFoundError(str(dataset_id))

    existing_job = session.exec(
        select(Job)
        .where(Job.dataset_id == dataset_id, Job.file_name == data.file_name)
    )

    if existing_job.first():
        raise JobWithFileNameAlreadyExistsError(data.file_name)

    job = Job(
        description=data.description,
        file_name=data.file_name,
        dataset_id=dataset_id,
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


@job_router.delete("/{job_id}")
async def delete_job(job_id: UUID, dataset_id: UUID, session: Session = Depends(get_session)) -> None:
    job = session.get(Job, job_id)
    if not job or job.dataset_id != dataset_id:
        raise DatasetNotFoundError(str(dataset_id))

    session.delete(job)
    session.commit()


@job_router.get("/{job_id}")
async def get_job(job_id: UUID, dataset_id: UUID, session: Session = Depends(get_session)) -> Job:
    job = session.get(Job, job_id)
    if not job or job.dataset_id != dataset_id:
        raise DatasetNotFoundError(str(dataset_id))

    return job


@job_router.put("/{job_id}")
async def update_job(job_id: UUID, dataset_id: UUID, data: UpdateJob, session: Session = Depends(get_session)) -> Job:
    job = session.get(Job, job_id)
    if not job or job.dataset_id != dataset_id:
        raise DatasetNotFoundError(str(dataset_id))

    job.description = data.description if data.description is not None else job.description
    job.file_name = data.file_name if data.file_name is not None else job.file_name
    job.generations = data.generations if data.generations is not None else job.generations
    job.population_size = data.population_size if data.population_size is not None else job.population_size
    job.max_expression_size = data.max_expression_size if data.max_expression_size is not None else job.max_expression_size
    job.tournament_size = data.tournament_size if data.tournament_size is not None else job.tournament_size
    job.crossover_probability = data.crossover_probability if data.crossover_probability is not None else job.crossover_probability
    job.mutation_probability = data.mutation_probability if data.mutation_probability is not None else job.mutation_probability
    job.loss_function = data.loss_function if data.loss_function is not None else job.loss_function
    job.max_optimization_iterations = data.max_optimization_iterations if data.max_optimization_iterations is not None else job.max_optimization_iterations
    job.max_optimization_restarts = data.max_optimization_restarts if data.max_optimization_restarts is not None else job.max_optimization_restarts
    job.parameter_count = data.parameter_count if data.parameter_count is not None else job.parameter_count
    job.split = data.split if data.split is not None else job.split
    job.simplify = data.simplify if data.simplify is not None else job.simplify

    session.add(job)
    session.commit()
    session.refresh(job)

    return job
