from pydantic import BaseModel

from core.repositories.base import BaseRepository
from core.models.outbox.outbox import Outbox


class OutboxRepository[T: BaseModel](BaseRepository[Outbox[T]]):
    """Repository for managing Outbox messages in the database."""
