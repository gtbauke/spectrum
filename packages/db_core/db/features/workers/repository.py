from datetime import datetime, timezone
from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from .model import WorkerHeartbeatORM


class WorkerHeartbeatRepository:
    """Thin repository for worker heartbeat upserts and queries.

    This repository is intentionally simple and does NOT go through the
    full domain-mapper-repository pipeline used elsewhere — heartbeats
    are an infrastructure concern, not a domain entity.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upsert(
        self,
        *,
        worker_id: str,
        worker_type: str,
        status: str,
        current_task: str | None,
        task_started_at: datetime | None,
        started_at: datetime,
    ) -> None:
        """Insert a heartbeat row or update it if the worker_id already exists."""
        now = datetime.now(tz=timezone.utc)

        stmt = pg_insert(WorkerHeartbeatORM).values(
            worker_id=worker_id,
            worker_type=worker_type,
            status=status,
            current_task=current_task,
            task_started_at=task_started_at,
            last_heartbeat=now,
            started_at=started_at,
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=["worker_id"],
            set_={
                "status": stmt.excluded.status,
                "current_task": stmt.excluded.current_task,
                "task_started_at": stmt.excluded.task_started_at,
                "last_heartbeat": stmt.excluded.last_heartbeat,
                "worker_type": stmt.excluded.worker_type,
            },
        )

        await self._session.execute(stmt)
        await self._session.commit()

    async def list_all(self) -> Sequence[WorkerHeartbeatORM]:
        """Return all registered heartbeats."""
        result = await self._session.execute(
            select(WorkerHeartbeatORM).order_by(WorkerHeartbeatORM.worker_type)
        )
        return result.scalars().all()

    async def remove(self, worker_id: str) -> None:
        """Delete the heartbeat row for a worker (used on clean shutdown)."""
        await self._session.execute(
            delete(WorkerHeartbeatORM).where(
                WorkerHeartbeatORM.worker_id == worker_id
            )
        )
        await self._session.commit()
