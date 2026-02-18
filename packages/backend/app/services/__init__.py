from pydantic import BaseModel

from app.services.datasets.datasets_service import DatasetsService
from app.services.models.models_service import ModelsService
from app.services.models.model_training_service import ModelTrainingService
from app.infra.file_storage import get_transactional_file_storage
from app.services.datasets.dataset_files_service import DatasetFilesService
from app.services.jobs.jobs_service import JobsService
from app.services.inference.inference_service import InferenceService
from app.services.outbox.outbox_service import OutboxService
from core.tasks.datasets.payload import DatasetProcessTaskPayload


def get_outbox_service[T: BaseModel](payload_type: type[T]) -> OutboxService[T]:
    return OutboxService[T](model_type=payload_type)


def get_datasets_service() -> DatasetsService:
    return DatasetsService(
        datasets_file_service=DatasetFilesService(),
        outbox_service=get_outbox_service(DatasetProcessTaskPayload),
        storage=get_transactional_file_storage(),
    )


def get_models_service() -> ModelsService:
    return ModelsService()


def get_model_training_service() -> ModelTrainingService:
    dataset_files_service = DatasetFilesService()

    return ModelTrainingService(
        dataset_files_service=dataset_files_service,
        jobs_service=get_jobs_service(),
        models_service=get_models_service(),
    )


def get_jobs_service() -> JobsService:
    return JobsService()


def get_inference_service() -> InferenceService:
    dataset_files_service = DatasetFilesService()

    return InferenceService(
        models_service=get_models_service(),
        datasets_service=get_datasets_service(),
        dataset_files_service=dataset_files_service,
    )
