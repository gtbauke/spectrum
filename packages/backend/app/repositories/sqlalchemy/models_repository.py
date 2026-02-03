from typing import Optional
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
