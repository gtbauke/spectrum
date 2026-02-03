from app.services.datasets_service import DatasetsService
from app.services.models_service import ModelsService
from app.infra.file_storage import get_file_storage
from app.infra.events import get_dataset_events_publisher


def get_datasets_service() -> DatasetsService:
    return DatasetsService(
        storage=get_file_storage(),
        datasets_event_publisher=get_dataset_events_publisher()
    )


def get_models_service() -> ModelsService:
    return ModelsService()
