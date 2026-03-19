from uuid import UUID
from fastapi import HTTPException, status


class JobRunNotFound(HTTPException):
    def __init__(self, job_run_id: UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job run with id {job_run_id} not found",
        )
