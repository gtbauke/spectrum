from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import func, select, update

from db.models.outbox import OutboxORM

from core.models.outbox.outbox import Outbox
from core.models.outbox.outbox_status import OutboxStatus

from workers.repositories.interfaces.worker_outbox_repository import AbstractWorkerOutboxRepository


class WorkerOutboxRepository(AbstractWorkerOutboxRepository):
    """
    Repository for managing Outbox messages specific to workers. This version
    is not generic because we do not care about the structure of the payload,
    we just need the payload to be JSON-serializable.
    """

    async def fetch_batch(self, batch_size: int = 100) -> list[Outbox[BaseModel]]:
        result = await self._session.execute(
            select(OutboxORM)
            .where(
                OutboxORM.status == OutboxStatus.PENDING,
                OutboxORM.available_at <= func.now(),
            )
            .order_by(OutboxORM.created_at.asc())
            .with_for_update(skip_locked=True)
            .limit(batch_size)
        )

        outbox_orms = result.scalars().all()
        return [Outbox[BaseModel].model_validate(outbox_orm) for outbox_orm in outbox_orms]

    async def batch_mark_as_published(self, ids: list[UUID]) -> None:
        await self._session.execute(
            update(OutboxORM)
            .where(OutboxORM.id.in_(ids))
            .values(
                status=OutboxStatus.PROCESSED,
                published_at=func.now()
            )
        )
