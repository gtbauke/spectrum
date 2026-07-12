import io
import logging
import os
import tempfile
from typing import Any
from uuid import UUID

from core.features.profiles.jobs.runs.events import RunFinishedEvent
from core.features.profiles.models.where import ModelWhere
from core.features.profiles.jobs.where import JobWhere
from core.features.datasets.where import DatasetWhere
from core.features.datasets.artifact_role import ArtifactRole
from core.ports.events.event_handler import EventHandler
from core.ports.events.message_broker import MessageBroker

from db.common.session import AsyncSessionLocal
from adapters.worker_unit_of_work import WorkerUnitOfWork
from services.validation_service import ValidationService

logger = logging.getLogger(__name__)


class RunFinishedHandler(EventHandler[RunFinishedEvent]):
    routing_key: str = "runs.finished"

    def __init__(
        self,
        *,
        broker: MessageBroker,
    ) -> None:
        self._broker = broker
        self._validation_service = ValidationService()

    def parse(self, payload: dict[str, Any]) -> RunFinishedEvent:
        return RunFinishedEvent.model_validate(payload)

    async def handle(self, event: RunFinishedEvent) -> None:
        logger.info(
            "Handling run finished event: run_id=%s | model_id=%s",
            event.run_id,
            event.model_id,
        )

        try:
            async with WorkerUnitOfWork(
                session_factory=AsyncSessionLocal,
                broker=self._broker,
            ) as uow:
                # 1. Resolve Model
                model = await uow.models.get_unique(ModelWhere(id=event.model_id))
                if not model:
                    logger.error("Model not found: model_id=%s",
                                 event.model_id)
                    return

                # 2. Resolve Job and Dataset
                job = await uow.jobs.get_unique(JobWhere(id=event.job_id))
                if not job:
                    logger.error("Job not found: job_id=%s", event.job_id)
                    return

                dataset = await uow.datasets.get_unique(DatasetWhere(id=job.runs_against))
                if not dataset:
                    logger.error(
                        "Dataset not found: dataset_id=%s", job.runs_against)
                    return

                # 3. Find validation artifact
                validation_artifacts = [
                    a for a in dataset.artifacts if a.role == ArtifactRole.VALIDATION
                ]

                group_by_columns = validation_artifacts[0].group_by_columns if validation_artifacts else None

                if not validation_artifacts:
                    logger.info(
                        "No validation artifact found for dataset %s. Skipping validation.", dataset.id)
                    return

                validation_artifact = validation_artifacts[0]

                # 4. Download necessary files
                with tempfile.TemporaryDirectory() as tmp_dir:
                    dataset_path = os.path.join(tmp_dir, "validation.csv")
                    model_path = os.path.join(tmp_dir, "model.egraph")

                    await uow.file_storage.download(path=validation_artifact.path, destination=dataset_path)
                    await uow.file_storage.download(path=model.path, destination=model_path)

                    # 5. Run validation
                    # Note: We need the results.csv path as well if we want to parse expressions from it.
                    # However, ValidationService as currently implemented uses Reggression.pareto()
                    # which should load them from the e-graph dump.

                    predictions_df, metrics = await self._validation_service.validate(
                        model=model,
                        model_egraph_path=model_path,  # Pass local path
                        validation_artifact_path=dataset_path,
                        group_by_columns=group_by_columns
                    )

                    # 6. Save CSV results (easier for frontend)
                    csv_buf = io.BytesIO()
                    predictions_df.to_csv(csv_buf, index=False)
                    csv_buf.seek(0)

                    output_dir = os.path.dirname(model.path)
                    csv_path = f"{output_dir}/validation_results.csv"

                    upload_result = await uow.file_storage.upload(
                        path=csv_path,
                        file=csv_buf,
                    )

                    logger.info("Validation CSV saved: %s", upload_result.path)

                    # 7. Update Model with results
                    model.validation_path = upload_result.path
                    model.metrics = metrics

                    await uow.models.update(model)
                    # Unit of Work will commit automatically

            logger.info("Validation completed for model %s", event.model_id)

        except Exception:
            logger.exception("Failed to validate model %s", event.model_id)
            # We don't mark the run as failed here because training already finished successfully.
            # Validation is a post-processing step.
