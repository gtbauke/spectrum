from fastapi import APIRouter, Depends, Form, UploadFile, File

from app.api.v1.schemas.dataset import CreateDatasetRequest, CreateDatasetResponse
from app.db.uow.unit_of_work import UnitOfWork
from app.api.deps import get_uow
from app.services.datasets_service import DatasetsService
from app.infra.file_storage import FileStorage, get_file_storage
from app.infra.events.datasets.dataset_events_publisher import DatasetsEventsPublisher
from app.infra.events import get_dataset_events_publisher
from app.services.dataset_files_service import DatasetFilesService

datasets_router = APIRouter(tags=["datasets"])


@datasets_router.post(
    path="/upload",
    response_model=CreateDatasetResponse,
    status_code=201,
)
async def create_dataset(
    name: str = Form(...),
    file: UploadFile = File(...),
    uow: UnitOfWork = Depends(get_uow),
    file_storage: FileStorage = Depends(get_file_storage),
    datasets_publisher: DatasetsEventsPublisher = Depends(
        get_dataset_events_publisher)
):
    payload = CreateDatasetRequest(name=name)
    service = DatasetsService(
        datasets_file_service=DatasetFilesService(
            file_storage=file_storage
        ),
        datasets_event_publisher=datasets_publisher
    )

    async with uow:
        dataset = await service.create(
            uow=uow,
            name=payload.name,
            file=file
        )

    return dataset
