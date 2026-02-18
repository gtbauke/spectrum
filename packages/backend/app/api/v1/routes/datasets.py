from uuid import UUID
from fastapi import APIRouter, Depends, Form, UploadFile, File

from app.api.v1.schemas.dataset import CreateDatasetRequest
from app.api.deps import get_uow
from app.services import get_datasets_service
from app.services.datasets.datasets_service import CreateDatasetData, DatasetSearchBy, DatasetsService
from app.api.v1.routes.jobs import jobs_router

from core.ports.unit_of_work import UnitOfWork
from core.models.datasets.dataset import Dataset

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
    datasets_service: DatasetsService = Depends(get_datasets_service),
):
    payload = CreateDatasetRequest(name=name)

    async with uow:
        dataset = await datasets_service.create(
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
    datasets_service: DatasetsService = Depends(get_datasets_service),
):
    async with uow:
        datasets = await datasets_service.get_all(uow=uow)

    return list(datasets)


@datasets_router.get(
    path="/{dataset_id}",
    response_model=Dataset,
)
async def get_dataset(
    dataset_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    datasets_service: DatasetsService = Depends(get_datasets_service),
):
    async with uow:
        dataset = await datasets_service.get_unique(
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
    datasets_service: DatasetsService = Depends(get_datasets_service),
):
    async with uow:
        await datasets_service.delete_unique(
            uow=uow,
            where=DatasetSearchBy(dataset_id=dataset_id)
        )

datasets_router.include_router(
    prefix="/{dataset_id}/jobs",
    router=jobs_router
)
