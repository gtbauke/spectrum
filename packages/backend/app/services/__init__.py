from app.services.datasets.datasets_service import DatasetsService
from app.services.models.models_service import ModelsService
from app.services.models.model_training_service import ModelTrainingService
from app.infra.file_storage import get_file_storage
from app.infra.events import get_dataset_events_publisher
from app.services.datasets.dataset_files_service import DatasetFilesService


def get_datasets_service() -> DatasetsService:
    return DatasetsService(
        datasets_file_service=DatasetFilesService(
            file_storage=get_file_storage().scoped(scope="datasets")
        ),
        datasets_event_publisher=get_dataset_events_publisher()
    )


def get_models_service() -> ModelsService:
    return ModelsService()


def get_model_training_service() -> ModelTrainingService:
    return ModelTrainingService()
