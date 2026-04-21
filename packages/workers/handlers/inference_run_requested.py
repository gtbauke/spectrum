import asyncio
import logging
import os
import tempfile
import time

from typing import Any
from uuid import UUID

from reggression import Reggression  # type: ignore

from iql.compiler import IqlCompiler
from iql.executor.query_executor import QueryExecutor

from core.features.profiles.blocks.inference.events import InferenceRunRequestedEvent
from core.features.profiles.blocks.inference.inference_result import InferenceResult
from core.features.profiles.blocks.inference.where import InferenceRunWhere
from core.features.profiles.models.where import ModelFilter
from core.features.datasets.where import DatasetWhere
from core.features.datasets.artifact_role import ArtifactRole
from core.features.profiles.blocks.inference.inference_run import InferenceRunStatus
from core.features.profiles.jobs.where import JobWhere

from core.utils.filters.field_filter import UUIDFilter

from core.ports.events.event_handler import EventHandler
from core.ports.events.message_broker import MessageBroker

from db.common.session import AsyncSessionLocal
from adapters.worker_unit_of_work import WorkerUnitOfWork

logger = logging.getLogger(__name__)


class InferenceRunRequestedHandler(EventHandler[InferenceRunRequestedEvent]):
    routing_key: str = "inference.run_requested"

    def __init__(self, *, broker: MessageBroker) -> None:
        self._broker = broker

    def parse(self, payload: dict[str, Any]) -> InferenceRunRequestedEvent:
        return InferenceRunRequestedEvent.model_validate(payload)

    async def handle(self, event: InferenceRunRequestedEvent) -> None:
        logger.info(
            "Handling inference run requested: run_id=%s | block_id=%s | query=%s",
            event.run_id,
            event.block_id,
            event.query
        )

        start_time = time.perf_counter()

        try:
            async with WorkerUnitOfWork(
                session_factory=AsyncSessionLocal,
                broker=self._broker,
            ) as uow:
                # Initial status: Resolving Models
                run = await uow.inference_runs.get_unique(InferenceRunWhere(id=event.run_id))
                if not run:
                    logger.error("Run %s not found in database", event.run_id)
                    return

                run.status = InferenceRunStatus.RESOLVING_MODELS
                await uow.inference_runs.update(run)
                await uow.commit()

                available_models = await uow.models.list_all(
                    filter=ModelFilter(
                        profile_id=UUIDFilter(eq=run.profile_id),
                    )
                )

                model_identifiers = [
                    m.name for m in available_models] + [str(m.id) for m in available_models]

                compiler = IqlCompiler()
                compilation_result = compiler.compile(
                    query=event.query,
                    available_models=model_identifiers,
                )

                run.status = InferenceRunStatus.DOWNLOADING_DATA
                await uow.inference_runs.update(run)
                await uow.commit()

                if not compilation_result.is_success:
                    raise ValueError(
                        f"Failed to compile query: {compilation_result.errors.errors[0]}"
                    )

                model_identifier = compilation_result.resolved_model_identifier
                if not model_identifier:
                    raise ValueError(
                        "No model identifier resolved during compilation")

                resolved_model = None
                for m in available_models:
                    if m.name == model_identifier or str(m.id) == model_identifier:
                        resolved_model = m
                        break

                if not resolved_model:
                    raise ValueError(
                        f"Resolved model identifier '{model_identifier}' does not match any available model"
                    )

                job = await uow.jobs.get_unique(JobWhere(id=resolved_model.generated_by))
                if not job:
                    raise ValueError(
                        f"Job '{resolved_model.generated_by}' not found")

                dataset = await uow.datasets.get_unique(DatasetWhere(id=job.runs_against))
                if not dataset:
                    raise ValueError(f"Dataset '{job.runs_against}' not found")

                data_artifacts = [
                    a for a in dataset.artifacts if a.role == ArtifactRole.DATA]

                if not data_artifacts:
                    raise ValueError(
                        f"No data artifact found for dataset '{dataset.id}'")

                dataset_artifact = data_artifacts[0]

                with tempfile.TemporaryDirectory() as tmp_dir:
                    dataset_path = os.path.join(tmp_dir, "dataset.csv")
                    model_path = os.path.join(tmp_dir, "model.egraph")

                    await uow.file_storage.download(path=dataset_artifact.path, destination=dataset_path)
                    await uow.file_storage.download(path=resolved_model.path, destination=model_path)

                    run.status = InferenceRunStatus.EXECUTING
                    await uow.inference_runs.update(run)
                    await uow.commit()

                    def run_heavy_execution():
                        if compilation_result.plan is None:
                            raise ValueError(
                                "No execution plan generated during compilation")

                        reggression = Reggression(
                            dataset=dataset_path, loadFrom=model_path)
                        executor = QueryExecutor(reggressions={
                            model_identifier: reggression}, plan=compilation_result.plan)

                        query_result = executor.execute()
                        return query_result

                    query_result = await asyncio.to_thread(run_heavy_execution)

                    logger.info("Inference execution completed for run %s. Got %d results.",
                                event.run_id, len(query_result.results))

                    logger.info(f"Sample results: {query_result.results[:10]}")

                    domain_results = [
                        InferenceResult.new(
                            run_id=event.run_id,
                            run_version=run.version,
                            expression=r.expression if r.expression else "",
                            fitness=r.fitness,
                            latex=r.latex,
                            numpy=r.numpy,
                            parameters={i: p for i, p in map(lambda _i: (str(_i[0]), _i[1]), enumerate(
                                r.parameters)) if p is not None} if r.parameters else None,
                            size=r.size,
                            frequency=r.frequency,
                            prediction=r.prediction,
                            egraph_id=str(
                                r.egraph_id) if r.egraph_id is not None else None,
                        ) for r in query_result.results
                    ]

                    await uow.inference_results.add_many(domain_results)

                end_time = time.perf_counter()
                execution_time_ms = int((end_time - start_time) * 1000)

                run.status = InferenceRunStatus.COMPLETED
                run.execution_time_ms = execution_time_ms

                await uow.inference_runs.update(run)
                await uow.commit()

                logger.info("Inference execution completed for run %s in %dms. Persisted %d results.",
                            event.run_id, execution_time_ms, len(domain_results))

        except Exception as e:
            logger.exception(
                "Failed to handle inference run requested for run %s", event.run_id)
            async with WorkerUnitOfWork(
                session_factory=AsyncSessionLocal,
                broker=self._broker,
            ) as uow:
                run = await uow.inference_runs.get_unique(InferenceRunWhere(id=event.run_id))
                if run:
                    run.status = InferenceRunStatus.FAILED
                    run.error = str(e)

                    await uow.inference_runs.update(run)
                    await uow.commit()
            raise
