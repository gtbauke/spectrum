from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select

from app.db.models.model import ModelORM
from app.repositories.models_repository import ModelsRepository


class SqlAlchemyModelsRepository(ModelsRepository):
    async def get_by_id(self, id: UUID) -> Optional[ModelORM]:
        result = await self._session.execute(
            select(ModelORM).where(ModelORM.id == id)
        )

        return result.scalar_one_or_none()

    async def get_for_update(self, id: UUID) -> ModelORM | None:
        statement = (
            select(ModelORM)
            .where(ModelORM.id == id)
            .with_for_update()
        )

        result = await self._session.execute(statement)
        orm = result.scalar_one_or_none()

        return orm

    async def add(self, obj: ModelORM) -> ModelORM:
        self._session.add(obj)
        await self._session.flush()

        return obj

    async def get_by_dataset_id(self, dataset_id: UUID) -> ModelORM | None:
        result = await self._session.execute(
            select(ModelORM).where(ModelORM.dataset_id == dataset_id)
        )

        return result.scalar_one_or_none()

    async def get_all_trained_models(self) -> Sequence[ModelORM]:
        result = await self._session.execute(
            select(ModelORM).where(ModelORM.model_file.isnot(None))
        )

        return result.scalars().all()

    async def get_all_non_trained_models(self) -> Sequence[ModelORM]:
        result = await self._session.execute(
            select(ModelORM).where(ModelORM.model_file.is_(None))
        )

        return result.scalars().all()
