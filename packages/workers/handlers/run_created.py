import io
import logging
import os
import tempfile

from datetime import datetime, timezone
from typing import Any

from core.features.datasets.artifact_role import ArtifactRole
from core.features.datasets.where import DatasetWhere
from core.features.profiles.jobs.runs.events import RunCreatedEvent, RunFinishedEvent
from core.features.profiles.jobs.runs.status import JobRunStatus
from core.features.profiles.jobs.runs.where import RunWhere
from core.features.profiles.jobs.where import JobWhere
from core.features.profiles.models.model import Model
from core.ports.events.event_handler import EventHandler
from core.ports.events.message_broker import MessageBroker

from services.heartbeat import HeartbeatService

from db.common.session import AsyncSessionLocal

from adapters.worker_unit_of_work import WorkerUnitOfWork
from services.training_service import TrainingService

logger = logging.getLogger(__name__)


class RunCreatedHandler(EventHandler[RunCreatedEvent]):
    routing_key: str = "runs.created"

    def __init__(
        self,
        *,
        broker: MessageBroker,
        heartbeat: HeartbeatService,
    ) -> None:
        self._broker = broker
        self._heartbeat = heartbeat
        self._training_service = TrainingService()

    def parse(self, payload: dict[str, Any]) -> RunCreatedEvent:
        return RunCreatedEvent.model_validate(payload)

    async def handle(self, event: RunCreatedEvent) -> None:
        logger.info(
            "Handling run created event: run_id=%s | version=%s | job_id=%s",
            event.run_id,
            event.version,
            event.job_id,
        )

        await self._heartbeat.set_busy(f"training run {event.run_id}")

        try:
            await self._handle_inner(event)
        finally:
            await self._heartbeat.set_idle()

    async def _handle_inner(self, event: RunCreatedEvent) -> None:

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

            job = await uow.jobs.get_unique(JobWhere(id=event.job_id))

            if not job:
                logger.error("Job not found: job_id=%s", event.job_id)
                return

            dataset = await uow.datasets.get_unique(
                DatasetWhere(id=job.runs_against),
            )

            if not dataset:
                logger.error("Dataset not found: dataset_id=%s",
                             job.runs_against)
                return

        logger.info("Run %s marked as RUNNING", event.run_id)

        data_artifacts = [
            a for a in dataset.artifacts if a.role == ArtifactRole.DATA
        ]

        if not data_artifacts:
            logger.error(
                "No data artifact found for dataset %s",
                dataset.id,
            )
            await self._mark_failed(where)
            return

        artifact_path = data_artifacts[0].path

        try:
            output_dir = f"profiles/{job.profile_id}/models/{event.run_id}"

            with tempfile.TemporaryDirectory() as tmp_dir:
                dataset_tmp_path = os.path.join(tmp_dir, "dataset.csv")
                dump_path = os.path.join(tmp_dir, "model.egraph")

                async with WorkerUnitOfWork(
                    session_factory=AsyncSessionLocal,
                    broker=self._broker,
                ) as uow:
                    logger.info("Downloading dataset for training from %s", artifact_path)
                    await uow.file_storage.download(
                        path=artifact_path,
                        destination=dataset_tmp_path,
                    )

                result = await self._training_service.train(
                    job=job,
                    artifact_path=dataset_tmp_path,
                    dump_path=dump_path,
                )

            logger.info("Training complete for run %s", event.run_id)

        except Exception:
            logger.exception("Run %s failed during training", event.run_id)
            await self._mark_failed(where)
            return

        try:
            async with WorkerUnitOfWork(
                session_factory=AsyncSessionLocal,
                broker=self._broker,
            ) as uow:
                results_file = io.BytesIO(result.results_csv)
                results_upload = await uow.file_storage.upload(
                    path=f"{output_dir}/results.csv",
                    file=results_file,
                )

                logger.info(
                    "Results CSV saved: %s (%d bytes)",
                    results_upload.path,
                    results_upload.size,
                )

                if result.egraph_dump:
                    egraph_file = io.BytesIO(result.egraph_dump)
                    egraph_upload = await uow.file_storage.upload(
                        path=f"{output_dir}/egraph.dump",
                        file=egraph_file,
                    )

                    logger.info(
                        "E-graph dump saved: %s (%d bytes)",
                        egraph_upload.path,
                        egraph_upload.size,
                    )
                else:
                    raise ValueError(
                        f"Missing e-graph dump from training results for run {event.run_id}")

                model = Model(
                    name=f"{job.name} - v{event.version}",
                    profile_id=job.profile_id,
                    generated_by=job.id,
                    path=egraph_upload.path,
                    metrics=None,
                    validation_path=None,
                )

                await uow.models.add(model)

                logger.info(
                    "Model created: id=%s, name=%s",
                    model.id,
                    model.name,
                )

                await uow.runs.update_status(
                    where=where,
                    status=JobRunStatus.FINISHED,
                    finished_at=datetime.now(tz=timezone.utc),
                )

                # Emit RunFinishedEvent to trigger validation
                validation_event = RunFinishedEvent(
                    run_id=event.run_id,
                    job_id=event.job_id,
                    model_id=model.id,
                )

                uow.events_publisher.publish(
                    routing_key=validation_event.routing_key,
                    payload=validation_event.model_dump(mode="json"),
                )

            logger.info("Run %s marked as FINISHED", event.run_id)

        except Exception:
            logger.exception(
                "Run %s failed during post-processing", event.run_id,
            )
            await self._mark_failed(where)

    async def _mark_failed(self, where: RunWhere) -> None:
        """Opens a fresh UoW scope to mark a run as FAILED."""
        async with WorkerUnitOfWork(
            session_factory=AsyncSessionLocal,
            broker=self._broker,
        ) as uow:
            await uow.runs.update_status(
                where=where,
                status=JobRunStatus.FAILED,
                finished_at=datetime.now(tz=timezone.utc),
            )

        logger.info("Run %s marked as FAILED", where.id)
