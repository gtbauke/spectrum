from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories.base import BaseRepository
from core.models.outbox.outbox import Outbox


class OutboxRepository[T: BaseModel](BaseRepository[Outbox[T]]):
    """Repository for managing Outbox messages in the database."""

    def __init__(self, session: AsyncSession, model_type: type[T]) -> None:
        super().__init__(session)
        self._model_type = model_type
