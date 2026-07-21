import asyncio
import logging

from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from db.features.workers.repository import WorkerHeartbeatRepository

logger = logging.getLogger(__name__)


class HeartbeatService:
    """Periodically upserts a heartbeat row into PostgreSQL.

    Handlers call :meth:`set_busy` / :meth:`set_idle` to update the
    status that gets written on the next heartbeat tick.
    """

    def __init__(
        self,
        *,
        worker_id: str,
        worker_type: str,
        session_factory,
        interval_seconds: int = 10,
    ) -> None:
        self._worker_id = worker_id
        self._worker_type = worker_type
        self._session_factory = session_factory
        self._interval = interval_seconds
        self._started_at = datetime.now(tz=timezone.utc)

        # Mutable state (set by handlers)
        self._status: str = "idle"
        self._current_task: str | None = None
        self._task_started_at: datetime | None = None

        self._task: asyncio.Task | None = None

    # -- Public API for handlers -----------------------------------------------

    async def set_busy(self, task_description: str) -> None:
        """Mark the worker as busy with a human-readable task description and flush immediately."""
        self._status = "busy"
        self._current_task = task_description
        self._task_started_at = datetime.now(tz=timezone.utc)
        try:
            await self._send_heartbeat()
        except Exception:
            logger.warning("Failed to flush heartbeat on set_busy", exc_info=True)

    async def set_idle(self) -> None:
        """Mark the worker as idle (no active task) and flush immediately."""
        self._status = "idle"
        self._current_task = None
        self._task_started_at = None
        try:
            await self._send_heartbeat()
        except Exception:
            logger.warning("Failed to flush heartbeat on set_idle", exc_info=True)

    # -- Lifecycle --------------------------------------------------------------

    def start(self) -> asyncio.Task:
        """Launch the background heartbeat loop."""
        self._task = asyncio.create_task(self._loop(), name=f"heartbeat-{self._worker_id}")
        return self._task

    async def stop(self) -> None:
        """Cancel the heartbeat loop and remove the row from the database."""
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

        # Best-effort cleanup
        try:
            async with self._session_factory() as session:
                repo = WorkerHeartbeatRepository(session)
                await repo.remove(self._worker_id)
                logger.info("Heartbeat row removed for worker '%s'", self._worker_id)
        except Exception:
            logger.warning("Failed to remove heartbeat row on shutdown", exc_info=True)

    # -- Internal ---------------------------------------------------------------

    async def _loop(self) -> None:
        """Send a heartbeat every ``interval`` seconds."""
        logger.info(
            "Heartbeat loop started for '%s' (every %ds)",
            self._worker_id, self._interval,
        )
        while True:
            try:
                await self._send_heartbeat()
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.warning("Heartbeat upsert failed", exc_info=True)

            await asyncio.sleep(self._interval)

    async def _send_heartbeat(self) -> None:
        async with self._session_factory() as session:
            repo = WorkerHeartbeatRepository(session)
            await repo.upsert(
                worker_id=self._worker_id,
                worker_type=self._worker_type,
                status=self._status,
                current_task=self._current_task,
                task_started_at=self._task_started_at,
                started_at=self._started_at,
            )
