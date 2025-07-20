from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select
from app.database import get_session
from app.resources.datasets.models import Dataset, CreateDataset
from app.resources.services.file_service import FileService
from app.resources.services.services import get_file_service

dataset_router = APIRouter(prefix="/datasets", tags=["datasets"])


@dataset_router.get("/")
def get_datasets(session: Session = Depends(get_session)) -> list[Dataset]:
    datasets = session.exec(select(Dataset)).all()
    return list(datasets)


@dataset_router.get("/{dataset_id}")
def get_dataset(dataset_id: str, session: Session = Depends(get_session)) -> Dataset:
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    return dataset


@dataset_router.post("/")
def create_dataset(data: CreateDataset, session: Session = Depends(get_session)) -> Dataset:
    dataset = Dataset(name=data.name, description=data.description,
                      dataset_file_path=data.dataset_file_path)

    session.add(dataset)
    session.commit()
    session.refresh(dataset)

    return dataset


@dataset_router.post("/{dataset_id}/upload")
async def upload_dataset_file(
    dataset_id: str,
    file: UploadFile = File(..., media_type="multipart/form-data"),
    session: Session = Depends(get_session),
    file_service: FileService = Depends(get_file_service)
):
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    MAX_FILE_SIZE = 100 * 1024 * 1024
    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    await file.seek(0)

    # TODO: Save the uploaded file to S3
    # For now, lets save to a local temporary directory
    try:
        file_path = file_service.upload_file(
            file.file, f"{dataset_id}/{file.filename}")

        dataset.dataset_file_path = file_path

        session.add(dataset)
        session.commit()
        session.refresh(dataset)

        return {
            "message": "File uploaded successfully",
            "file_path": file_path,
            "filename": file.filename,
            "dataset_id": dataset_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"File upload failed: {str(e)}")
