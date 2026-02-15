from uuid import UUID

from app.api.deps import UnitOfWork
from app.domain.models.model import Model
from app.domain.jobs.job import Job
from app.db.models.model import ModelORM

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
            orm = await uow.models.get_by_id(model_id)

            if not orm:
                raise ValueError(f"Model with ID {model_id} not found.")

            domain = orm.to_domain()

        return domain

    async def get_with_job(
        self,
        uow: UnitOfWork,
        *,
        model_id: UUID,
    ) -> tuple[Model, Job]:
        async with uow:
            result = await uow.models.get_with_job(model_id)

            if not result:
                raise ValueError(f"Model with ID {model_id} not found.")

            model_orm, job_orm = result

            model_domain = model_orm.to_domain()
            job_domain = job_orm.to_domain()

        return model_domain, job_domain

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
                return existing_model.to_domain()

            if not existing_job:
                raise ValueError(f"Job with ID {job_id} not found.")

            orm = await uow.models.add(ModelORM(
                name=model_name,
                dataset_id=dataset_id,
                job_id=job_id,
            ))

            domain = orm.to_domain()

        return domain

    async def list(
        self,
        uow: UnitOfWork,
    ) -> list[Model]:
        async with uow:
            orms = await uow.models.list_all()
            domains = [orm.to_domain() for orm in orms]

        return domains

    async def update_model_file_path(
        self,
        uow: UnitOfWork,
        *,
        model_id: UUID,
        model_file_path: str,
    ) -> Model:
        async with uow:
            orm = await uow.models.get_by_id(model_id)

            if not orm:
                raise ValueError(f"Model with ID {model_id} not found.")

            orm.model_file = model_file_path
            domain = orm.to_domain()

            await uow.models.update(orm)

        return domain
