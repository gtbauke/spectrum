from uuid import UUID
from pydantic import BaseModel

from sqlalchemy import select, delete
from app.db.models.outbox import OutboxORM

from core.models.outbox.outbox import Outbox
from core.repositories.outbox_repository import OutboxRepository

# TODO: remove type ignore in list_all method
# to do that, we need to pass the payload type on repository __init__
# this means we actually need a repository factory in the unit of work
# or we need different repositories for different payload types, what could be overkill


class SqlAlchemyOutboxRepository[T: BaseModel](OutboxRepository[T]):
    """SQLAlchemy implementation of the OutboxRepository."""

    async def get_by_id(self, id: UUID) -> Outbox[T] | None:
        return await self._session.get(Outbox[T], id)

    async def get_for_update(self, id: UUID) -> Outbox[T] | None:
        return await self._session.get(Outbox[T], id, with_for_update=True)

    async def add(self, obj: Outbox[T]) -> Outbox[T]:
        orm = OutboxORM.from_domain(obj)

        self._session.add(orm)
        await self._session.flush()

        return obj

    async def update(self, obj: Outbox[T]) -> Outbox[T]:
        orm = OutboxORM.from_domain(obj)

        await self._session.merge(orm)
        await self._session.flush()

        return obj

    async def delete(self, id: UUID) -> None:
        await self._session.execute(
            delete(OutboxORM).where(OutboxORM.id == id)
        )

    async def list_all(self, where_id: UUID | None = None) -> list[Outbox[T]]:
        query = select(OutboxORM)
        if where_id:
            query = query.where(OutboxORM.aggregate_id == where_id)

        result = await self._session.execute(query)

        return [obj.to_domain(T)  # type: ignore
                for obj in result.scalars().all()]
