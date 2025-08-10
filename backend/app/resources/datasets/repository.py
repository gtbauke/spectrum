from sqlmodel import Session, select
from fastapi import UploadFile
from uuid import UUID

from app.utils.id import ID
from app.resources.datasets.models import Dataset, CreateDataset, DatasetFileUploadResponse
from app.resources.datasets.errors import DatasetNotFoundError, NoFileProvidedError, FileTooLargeError, FileUploadError
from app.resources.jobs.repository import create_default_job

from app.services.file_service.file_service import FileService


async def get_all_datasets(session: Session):
    """
    Fetch all datasets along with their associated jobs.
    """
    query = select(Dataset)
    datasets = session.exec(query).all()

    return datasets


async def get_dataset_by_id(dataset_id: UUID, session: Session):
    """
    Fetch a dataset by its ID.
    """
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        raise DatasetNotFoundError(dataset_id)

    return dataset


async def create_dataset(data: CreateDataset, session: Session):
    """
    Create a new dataset.
    """
    dataset = Dataset(
        name=data.name,
        description=data.description,
        dataset_file_path=data.dataset_file_path
    )

    session.add(dataset)
    session.commit()
    session.refresh(dataset)

    return dataset


async def upload_data_file_to_dataset(
    dataset_id: ID,
    file: UploadFile,
    session: Session,
    file_service: FileService
):
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        raise DatasetNotFoundError(dataset_id)

    if not file.filename:
        raise NoFileProvidedError()

    if file.size is not None and file.size > file_service.MAX_FILE_SIZE:
        raise FileTooLargeError(file_service.MAX_FILE_SIZE)

    try:
        file_path = file_service.upload_file(
            file.file, f"{dataset_id}/{file.filename}")
        dataset.dataset_file_path = file_path

        session.add(dataset)
        session.commit()
        session.refresh(dataset)

        default_job = await create_default_job(dataset_id, session)
        # TODO: create a queue and add the job to it

        return DatasetFileUploadResponse(
            dataset=dataset,
            default_job=default_job
        )
    except Exception as e:
        raise FileUploadError(f"Failed to upload file: {str(e)}")
