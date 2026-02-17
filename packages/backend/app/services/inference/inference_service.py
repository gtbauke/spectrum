import logging
from uuid import UUID

from app.api.deps import UnitOfWork
from app.domain.inference.inference_session import InferenceSession
from app.services.models.models_service import ModelsService
from app.services.models.model_files_service import ModelFilesService
from app.services.datasets.datasets_service import DatasetSearchBy, DatasetsService
from app.services.datasets.dataset_files_service import DatasetFilesService
from app.domain.inference.live_model import LiveModel


logger = logging.getLogger(__name__)


class InferenceService:
    def __init__(
        self,
        models_service: ModelsService,
        datasets_service: DatasetsService,
        model_files_service: ModelFilesService,
        dataset_files_service: DatasetFilesService,
    ):
        self._models_service = models_service
        self._datasets_service = datasets_service
        self._model_files_service = model_files_service
        self._dataset_files_service = dataset_files_service

    async def create_inference_session(self, uow: UnitOfWork, *, model_id: UUID):
        async with uow:
            model = await self._models_service.get(uow=uow, model_id=model_id)
            dataset = await self._datasets_service.get_unique(uow=uow, where=DatasetSearchBy(dataset_id=model.dataset_id))

            if not model or not dataset or not model.job:
                raise ValueError("Model or Dataset not found")

            if model.model_file is None:
                raise ValueError(
                    "Model does not have associated model artifacts")

            if dataset.file_path is None:
                raise ValueError("Dataset does not have associated data file")

            model_path = await self._model_files_service.get_model_file_path(
                dataset_id=dataset.id,
                job_id=model.job.id,
            )

            dataset_path = await self._dataset_files_service.get_dataset_file_path(
                dataset_id=dataset.id,
                file_name=dataset.file_path
            )

            logger.info("Creating inference session for model %s and dataset %s", model.id, dataset.id, extra={
                "model_id": str(model.id),
                "dataset_id": str(dataset.id),
                "model_path": model_path,
                "dataset_path": dataset_path,
            })

            live_model = LiveModel(
                model=model,
                dataset=dataset,
                model_path=model_path,
                dataset_path=dataset_path,
            )

            session = InferenceSession(model=model, live_model=live_model)

        return session
