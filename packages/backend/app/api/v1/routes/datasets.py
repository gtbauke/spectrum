from uuid import UUID
from fastapi import APIRouter, Depends, Form, UploadFile, File

from app.api.v1.schemas.dataset import CreateDatasetRequest
from app.db.uow.unit_of_work import UnitOfWork
from app.api.deps import get_uow
from app.services.datasets.datasets_service import CreateDatasetData, DatasetSearchBy, DatasetsService
from app.infra.file_storage import FileStorage, get_file_storage
from app.infra.events.datasets.dataset_events_publisher import DatasetsEventsPublisher
from app.infra.events import get_dataset_events_publisher
from app.services.datasets.dataset_files_service import DatasetFilesService
from core.models.datasets.dataset import Dataset
from app.api.v1.routes.jobs import jobs_router

datasets_router = APIRouter(tags=["datasets"])


@datasets_router.post(
    path="/upload",
    response_model=Dataset,
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
            file_storage=file_storage.scoped("datasets")
        ),
        datasets_event_publisher=datasets_publisher
    )

    async with uow:
        dataset = await service.create(
            uow=uow,
            data=CreateDatasetData(
                name=payload.name,
                file=file,
            )
        )

    return dataset


@datasets_router.get(
    path="/",
    response_model=list[Dataset],
)
async def list_datasets(
    uow: UnitOfWork = Depends(get_uow),
    file_storage: FileStorage = Depends(get_file_storage),
    datasets_publisher: DatasetsEventsPublisher = Depends(
        get_dataset_events_publisher)
):
    service = DatasetsService(
        datasets_file_service=DatasetFilesService(
            file_storage=file_storage.scoped("datasets")
        ),
        datasets_event_publisher=datasets_publisher
    )

    async with uow:
        datasets = await service.get_all(uow=uow)

    return datasets


@datasets_router.get(
    path="/{dataset_id}",
    response_model=Dataset,
)
async def get_dataset(
    dataset_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    file_storage: FileStorage = Depends(get_file_storage),
    datasets_publisher: DatasetsEventsPublisher = Depends(
        get_dataset_events_publisher)
):
    service = DatasetsService(
        datasets_file_service=DatasetFilesService(
            file_storage=file_storage.scoped("datasets")
        ),
        datasets_event_publisher=datasets_publisher
    )

    async with uow:
        dataset = await service.get_unique(
            uow=uow,
            where=DatasetSearchBy(dataset_id=dataset_id)
        )

    return dataset


@datasets_router.delete(
    path="/{dataset_id}",
    status_code=204,
)
async def delete_dataset(
    dataset_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    file_storage: FileStorage = Depends(get_file_storage),
    datasets_publisher: DatasetsEventsPublisher = Depends(
        get_dataset_events_publisher)
):
    service = DatasetsService(
        datasets_file_service=DatasetFilesService(
            file_storage=file_storage.scoped("datasets")
        ),
        datasets_event_publisher=datasets_publisher
    )

    async with uow:
        await service.delete_unique(
            uow=uow,
            where=DatasetSearchBy(dataset_id=dataset_id)
        )

datasets_router.include_router(
    prefix="/{dataset_id}/jobs",
    router=jobs_router
)
