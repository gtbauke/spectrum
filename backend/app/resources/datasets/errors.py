from fastapi import HTTPException
from uuid import UUID


class DatasetNotFoundError(HTTPException):
    def __init__(self, dataset_id: str | UUID):
        super().__init__(status_code=404,
                         detail=f"Dataset with ID {dataset_id} not found.")
        self.dataset_id = dataset_id


class NoFileProvidedError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="No file provided.")


class FileTooLargeError(HTTPException):
    def __init__(self, max_size: int):
        super().__init__(status_code=413,
                         detail=f"File too large. Maximum allowed size is {max_size} bytes.")
        self.max_size = max_size


class FileUploadError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=500,
                         detail=f"File upload failed: {message}")
        self.message = message
