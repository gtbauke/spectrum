import logging

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from core.features.profiles.jobs.runs.events import RunCreatedEvent
from core.features.profiles.jobs.runs.status import JobRunStatus
from core.features.profiles.jobs.runs.where import RunWhere
from core.ports.events.event_handler import EventHandler
from core.ports.events.message_broker import MessageBroker

from db.common.session import AsyncSessionLocal

from adapters.worker_unit_of_work import WorkerUnitOfWork

logger = logging.getLogger(__name__)


class RunCreatedHandler(EventHandler[RunCreatedEvent]):
    routing_key: str = "runs.created"

    def __init__(
        self,
        *,
        broker: MessageBroker,
    ) -> None:
        self._broker = broker

    def parse(self, payload: dict[str, Any]) -> RunCreatedEvent:
        return RunCreatedEvent.model_validate(payload)

    async def handle(self, event: RunCreatedEvent) -> None:
        logger.info(
            "Handling run created event: run_id=%s | version=%s | job_id=%s",
            event.run_id,
            event.version,
            event.job_id,
        )

        where = RunWhere(id=event.run_id, version=event.version)

        async with WorkerUnitOfWork(
            session_factory=AsyncSessionLocal,
            broker=self._broker,
        ) as uow:
            run = await uow.runs.update_status(
                where=where,
                status=JobRunStatus.RUNNING,
                started_at=datetime.now(tz=timezone.utc),
            )

            if not run:
                logger.error("Run not found: run_id=%s", event.run_id)
                return

        logger.info("Run %s marked as RUNNING", event.run_id)

        # TODO: Execute model training logic here (eggp library).
        # The training result file should be saved via uow.file_storage.

        try:
            # Placeholder for training execution
            await self._execute_training(
                run_id=event.run_id,
                job_id=event.job_id,
            )

            async with WorkerUnitOfWork(
                session_factory=AsyncSessionLocal,
                broker=self._broker,
            ) as uow:
                await uow.runs.update_status(
                    where=where,
                    status=JobRunStatus.FINISHED,
                    finished_at=datetime.now(tz=timezone.utc),
                )

            logger.info("Run %s marked as FINISHED", event.run_id)

        except Exception:
            logger.exception("Run %s failed during training", event.run_id)

            async with WorkerUnitOfWork(
                session_factory=AsyncSessionLocal,
                broker=self._broker,
            ) as uow:
                await uow.runs.update_status(
                    where=where,
                    status=JobRunStatus.FAILED,
                    finished_at=datetime.now(tz=timezone.utc),
                )

            logger.info("Run %s marked as FAILED", event.run_id)

    async def _execute_training(
        self,
        *,
        run_id: UUID,
        job_id: UUID,
    ) -> None:
        """Placeholder for actual model training logic using eggp library."""
        logger.info(
            "Training placeholder for run_id=%s, job_id=%s",
            run_id,
            job_id,
        )
