from fastapi import APIRouter, Depends, UploadFile, File
from sqlmodel import Session
from uuid import UUID

from app.database import get_session
from app.utils.id import ID
from app.resources.datasets.models import CreateDataset, DatasetWithJobs, DatasetFileUploadResponse
from app.services.file_service.file_service import FileService
from app.services import get_file_service
from app.utils.api_response import ApiResponse

from app.resources.datasets.repository import get_all_datasets, get_dataset_by_id, create_dataset, upload_data_file_to_dataset

dataset_router = APIRouter(prefix="/datasets", tags=["datasets"])


@dataset_router.get("/", response_model=ApiResponse[list[DatasetWithJobs]])
async def get_datasets(session: Session = Depends(get_session)):
    datasets = await get_all_datasets(session)
    return {"data": datasets}


@dataset_router.get("/{dataset_id}", response_model=ApiResponse[DatasetWithJobs])
async def get_dataset(dataset_id: str, session: Session = Depends(get_session)):
    dataset = await get_dataset_by_id(UUID(dataset_id), session)
    return {"data": dataset}


@dataset_router.post("/", status_code=201, response_model=ApiResponse[DatasetWithJobs])
async def create_dataset_(data: CreateDataset, session: Session = Depends(get_session)):
    dataset = await create_dataset(data, session)
    return {"data": dataset}


@dataset_router.post("/{dataset_id}/upload", response_model=ApiResponse[DatasetFileUploadResponse])
async def upload_dataset_file(
    dataset_id: ID,
    file: UploadFile = File(..., media_type="multipart/form-data"),
    session: Session = Depends(get_session),
    file_service: FileService = Depends(get_file_service)
):
    response = await upload_data_file_to_dataset(
        dataset_id,
        file,
        session,
        file_service
    )

    return {"data": response}


@dataset_router.get("/{dataset_id}/top-expressions")
def get_top_expressions(dataset_id: str, n: int = 10):
    pass
