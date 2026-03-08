from uuid import UUID

from fastapi import HTTPException, status


class DatasetNotFound(HTTPException):
    def __init__(self, dataset_id: UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset with id '{dataset_id}' not found.",
        )
