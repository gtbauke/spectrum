from abc import abstractmethod
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.outbox.outbox import Outbox
from core.repositories.outbox_repository import OutboxRepository
from workers.repositories.errors.worker_should_not_call_error import WorkerShouldNotCallMethodError


class AbstractWorkerOutboxRepository(OutboxRepository[BaseModel]):
    """
    Repository for managing Outbox messages specific to workers. This version
    is not generic because we do not care about the structure of the payload,
    we just need the payload to be JSON-serializable.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session, BaseModel)

    async def get_by_id(self, id: UUID) -> Outbox[BaseModel] | None:
        raise WorkerShouldNotCallMethodError("get_by_id")

    async def get_for_update(self, id: UUID) -> Outbox[BaseModel] | None:
        raise WorkerShouldNotCallMethodError("get_for_update")

    async def add(self, obj: Outbox[BaseModel]) -> Outbox[BaseModel]:
        raise WorkerShouldNotCallMethodError("add")

    async def update(self, obj: Outbox[BaseModel]) -> Outbox[BaseModel]:
        raise WorkerShouldNotCallMethodError("update")

    async def delete(self, id: UUID) -> None:
        raise WorkerShouldNotCallMethodError("delete")

    async def list_all(self, where_id: UUID | None = None) -> list[Outbox[BaseModel]]:
        raise WorkerShouldNotCallMethodError("list_all")

    @abstractmethod
    async def fetch_batch(self, batch_size: int = 100) -> list[Outbox[BaseModel]]:
        """
        Fetch a batch of Outbox messages for processing. This method should be
        implemented by the concrete repository to retrieve messages in a way
        that is efficient for the worker's processing needs.
        """
        pass

    @abstractmethod
    async def batch_mark_as_published(self, ids: list[UUID]) -> None:
        """
        Mark a batch of Outbox messages as published. This method should be
        implemented by the concrete repository to update the status of messages
        after they have been successfully published.
        """
        pass
