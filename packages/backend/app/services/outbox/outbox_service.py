from typing import Sequence
from pydantic import BaseModel

from app.services.outbox.utils.create_outbox import CreateOutboxData
from app.services.outbox.utils.outbox_search_by import OutboxSearchBy
from app.services.outbox.utils.update_outbox import UpdateOutboxData

from core.models.outbox.outbox import Outbox
from core.ports.unit_of_work import UnitOfWork
from core.services.base import BaseService


class OutboxService[T: BaseModel](BaseService[
    Outbox[T],
    OutboxSearchBy,
    CreateOutboxData[T],
    UpdateOutboxData[T],
]):
    """
    Service for handling outbox messages.
    """

    def __init__(self, model_type: type[T]) -> None:
        super().__init__()
        self._model_type = model_type

    # TODO: implement get_unique in repository
    # and resolve the where parameter to filter
    # by the property specified in the where parameter
    async def get_unique(
        self,
        *,
        uow: UnitOfWork,
        where: OutboxSearchBy
    ) -> Outbox[T] | None:
        async with uow:
            repo = await uow.get_outbox_repository(self._model_type)
            return await repo.get_by_id(id=where.resolve())

    async def create(self, *, uow: UnitOfWork, data: CreateOutboxData[T]) -> Outbox[T]:
        async with uow:
            repo = await uow.get_outbox_repository(self._model_type)

            outbox = Outbox[T].create(
                aggregate_type=data.aggregate_type,
                aggregate_id=data.aggregate_id,
                event_type=data.event_type,
                event_version=data.event_version,
                payload=data.payload,
                available_at=data.available_at,
            )

            await repo.add(outbox)
            return outbox

    async def update_unique(self, *, uow: UnitOfWork, where: OutboxSearchBy, data: UpdateOutboxData[T]) -> Outbox[T]:
        async with uow:
            repo = await uow.get_outbox_repository(self._model_type)
            outbox = await repo.get_by_id(id=where.resolve())

            if not outbox:
                raise ValueError("Outbox message not found")

            updated_outbox = outbox.model_copy(
                update=data.model_dump(exclude_unset=True))

            await repo.update(updated_outbox)
            return updated_outbox

    async def delete_unique(self, *, uow: UnitOfWork, where: OutboxSearchBy):
        async with uow:
            repo = await uow.get_outbox_repository(self._model_type)
            await repo.delete(id=where.resolve())

    async def get_all(self, *, uow: UnitOfWork) -> Sequence[Outbox[T]]:
        async with uow:
            repo = await uow.get_outbox_repository(self._model_type)
            return await repo.list_all()
