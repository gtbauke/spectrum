from typing import Optional
from uuid import UUID

from sqlalchemy import select, delete

from app.db.models.model import ModelORM
from app.db.models.job import JobORM

from core.models.jobs.job import Job
from core.models.models.model import Model
from core.repositories.models_repository import ModelsRepository


class SqlAlchemyModelsRepository(ModelsRepository):
    async def get_by_id(self, id: UUID) -> Optional[Model]:
        result = await self._session.execute(
            select(ModelORM).where(ModelORM.id == id)
        )

        obj = result.scalar_one_or_none()
        return obj.to_domain() if obj else None

    async def get_for_update(self, id: UUID) -> Model | None:
        statement = (
            select(ModelORM)
            .where(ModelORM.id == id)
            .with_for_update()
        )

        result = await self._session.execute(statement)
        orm = result.scalar_one_or_none()

        return orm.to_domain() if orm else None

    async def add(self, obj: Model) -> Model:
        self._session.add(ModelORM.from_domain(obj))
        await self._session.flush()

        return obj

    async def get_by_dataset_id(self, dataset_id: UUID) -> Model | None:
        result = await self._session.execute(
            select(ModelORM).where(ModelORM.dataset_id == dataset_id)
        )

        obj = result.scalar_one_or_none()
        return obj.to_domain() if obj else None

    async def list_all(self, where_id: Optional[UUID] = None) -> list[Model]:
        query = select(ModelORM)
        if where_id:
            query = query.where(ModelORM.id == where_id)

        result = await self._session.execute(query)

        return [obj.to_domain() for obj in result.scalars().all()]

    async def update(self, obj: Model) -> Model:
        await self._session.merge(ModelORM.from_domain(obj))
        await self._session.flush()

        return obj

    async def delete(self, id: UUID) -> None:
        await self._session.execute(
            delete(ModelORM).where(ModelORM.id == id)
        )

    async def get_with_job(self, model_id: UUID) -> tuple[Model, Job] | None:
        result = await self._session.execute(
            select(ModelORM, JobORM)
            .join(JobORM, ModelORM.job_id == JobORM.id)
            .where(ModelORM.id == model_id)
        )

        row = result.one_or_none()

        if row is None:
            return None

        model_orm, job_orm = row
        return model_orm.to_domain(), job_orm.to_domain()
