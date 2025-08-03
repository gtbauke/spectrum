from fastapi import HTTPException
from app.utils.id import ID


class DatasetNotFoundError(HTTPException):
    def __init__(self, dataset_id: ID):
        super().__init__(status_code=404,
                         detail=f"Dataset with ID {dataset_id} not found")


class JobWithFileNameAlreadyExistsError(HTTPException):
    def __init__(self, file_name: str):
        super().__init__(status_code=400,
                         detail=f"Job with file name '{file_name}' already exists for this dataset")


class JobNotFoundError(HTTPException):
    def __init__(self, job_id: ID):
        super().__init__(status_code=404,
                         detail=f"Job with ID {job_id} not found")
