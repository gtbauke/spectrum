import asyncio
import logging
import os
import tempfile
import time

from typing import Any, cast
from uuid import UUID

from reggression import Reggression  # type: ignore

from iql.tokenizer.tokenizer import QueryTokenizer
from iql.parser.parser import InferenceQueryParser
from iql.parser.ast.select import SelectClauseAstNode
from iql.executor.query_executor import QueryExecutor

from core.features.profiles.blocks.inference.events import InferenceRunRequestedEvent
from core.features.profiles.blocks.inference.inference_result import InferenceResult
from core.features.profiles.blocks.inference.where import InferenceRunWhere
from core.features.profiles.models.where import ModelWhere, ModelFilter
from core.features.datasets.where import DatasetWhere
from core.features.datasets.artifact_role import ArtifactRole
from core.features.profiles.blocks.inference.inference_run import InferenceRunStatus

from core.utils.filters.field_filter import StringFilter, UUIDFilter

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

                # 1. Parse Query to find referenced model
                tokenizer = QueryTokenizer(event.query)
                tokens = tokenizer.tokenize()
                parser = InferenceQueryParser(tokens)
                root_node = parser.parse_expression()

                if not isinstance(root_node, SelectClauseAstNode):
                    raise ValueError("Query must be a SELECT statement")

                model_identifier = root_node.from_clause().identifier().name()
                logger.info("Query references model: %s", model_identifier)

                # 2. Resolve Model
                # Try by ID first, then by name
                model = None
                try:
                    model_id = UUID(model_identifier)
                    model = await uow.models.get_unique(ModelWhere(id=model_id))
                except ValueError:
                    # Not a UUID, search by name
                    models = await uow.models.list_all(ModelFilter(
                        profile_id=UUIDFilter(eq=run.profile_id)
                    ))

                    logger.info("Found %d models with name '%s'", len(models), model_identifier, extra={
                        "models": [m.name for m in models]
                    })

                    same_name_models = [
                        m for m in models if m.name == model_identifier]
                    if len(same_name_models) == 1:
                        model = same_name_models[0]

                if not model:
                    raise ValueError(f"Model '{model_identifier}' not found")

                run.status = InferenceRunStatus.DOWNLOADING_DATA
                await uow.inference_runs.update(run)
                await uow.commit()

                # 3. Resolve Dataset for this model
                if not model.generated_by:
                    raise ValueError(
                        f"Model '{model.id}' has no associated Job (generated_by is null)")

                from core.features.profiles.jobs.where import JobWhere
                job = await uow.jobs.get_unique(JobWhere(id=model.generated_by))

                if not job:
                    raise ValueError(
                        f"Job '{model.generated_by}' not found for model '{model.id}'")

                dataset = await uow.datasets.get_unique(DatasetWhere(id=job.runs_against))
                if not dataset:
                    raise ValueError(f"Dataset '{job.runs_against}' not found")

                data_artifacts = [
                    a for a in dataset.artifacts if a.role == ArtifactRole.DATA]

                if not data_artifacts:
                    raise ValueError(
                        f"No data artifact found for dataset '{dataset.id}'")

                dataset_artifact = data_artifacts[0]

                # 4. Download files
                with tempfile.TemporaryDirectory() as tmp_dir:
                    dataset_path = os.path.join(tmp_dir, "dataset.csv")
                    model_path = os.path.join(tmp_dir, "model.egraph")

                    # Download dataset CSV
                    await uow.file_storage.download(path=dataset_artifact.path, destination=dataset_path)
                    # Download model result (e-graph)
                    await uow.file_storage.download(path=model.path, destination=model_path)

                    run.status = InferenceRunStatus.EXECUTING
                    await uow.inference_runs.update(run)
                    await uow.commit()

                    def run_heavy_execution():
                        # 5. Initialize Reggression and Executor
                        reggression = Reggression(
                            dataset=dataset_path, loadFrom=model_path)
                        executor = QueryExecutor(root_node=root_node, reggressions={
                            model_identifier: reggression})

                        # 6. Execute
                        query_result = executor.execute()
                        return query_result

                    query_result = await asyncio.to_thread(run_heavy_execution)

                    # 7. Persist Results
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
