from uuid import UUID

from app.api.deps import UnitOfWork

from core.models.jobs.job_run import JobRun
from core.models.models.model import Model
from core.models.jobs.job_status import JobStatus

# TODO: better error handling in the Repository layer


class ModelsService:
    def __init__(self):
        pass

    async def get(
        self,
        uow: UnitOfWork,
        *,
        model_id: UUID,
    ) -> Model:
        async with uow:
            model = await uow.models.get_by_id(model_id)

            if not model:
                raise ValueError(f"Model with ID {model_id} not found.")

            return model

    async def update_model_job_status(
        self,
        uow: UnitOfWork,
        *,
        model_id: UUID,
        job_status: JobStatus,
    ) -> Model:
        async with uow:
            model = await uow.models.get_for_update(model_id)

            if not model:
                raise ValueError(f"Model with ID {model_id} not found.")

            updated_model = model.model_copy(
                update={
                    "status": job_status,
                }
            )

            await uow.models.update(updated_model)
            return updated_model

    async def create(
        self,
        uow: UnitOfWork,
        *,
        model_name: str,
        dataset_id: UUID,
        job_id: UUID,
    ) -> Model:
        async with uow:
            existing_model = await uow.models.get_by_dataset_id(dataset_id)
            existing_job = await uow.jobs.get_by_id(job_id)

            if existing_model:
                return existing_model

            if not existing_job:
                raise ValueError(f"Job with ID {job_id} not found.")

            model = Model.create(
                name=model_name,
                dataset_id=dataset_id,
                job=existing_job,
            )

            await uow.models.add(model)
            return model

    async def list(
        self,
        uow: UnitOfWork,
    ) -> list[Model]:
        async with uow:
            return await uow.models.list_all()

    async def update_model_file_path(
        self,
        uow: UnitOfWork,
        *,
        model_id: UUID,
        model_file_path: str,
    ) -> Model:
        async with uow:
            model = await uow.models.get_by_id(model_id)

            if not model:
                raise ValueError(f"Model with ID {model_id} not found.")

            updated_model = model.model_copy(
                update={
                    "model_file": model_file_path,
                }
            )

            await uow.models.update(updated_model)
            return updated_model

    async def record_model_job_run(
        self,
        uow: UnitOfWork,
        *,
        model_id: UUID,
    ) -> None:
        async with uow:
            model = await uow.models.get_by_id(model_id)

            if not model:
                raise ValueError(f"Model with ID {model_id} not found.")

            if not model.job:
                raise ValueError(
                    f"Model with ID {model_id} has no associated job.")

            job_run = JobRun.create(
                model_id=model_id,
                started_at=model.job.started_at,
                finished_at=model.job.finished_at,
            )

            await uow.job_runs.add(job_run)

    async def delete(
        self,
        uow: UnitOfWork,
        *,
        model_id: UUID,
    ) -> None:
        async with uow:
            await uow.models.delete(model_id)
