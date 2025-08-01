from fastapi import HTTPException


class DatasetNotFoundError(HTTPException):
    def __init__(self, dataset_id: str):
        super().__init__(status_code=404,
                         detail=f"Dataset with ID {dataset_id} not found")


class JobWithFileNameAlreadyExistsError(HTTPException):
    def __init__(self, file_name: str):
        super().__init__(status_code=400,
                         detail=f"Job with file name '{file_name}' already exists for this dataset")
