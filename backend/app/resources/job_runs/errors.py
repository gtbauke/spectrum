from fastapi import HTTPException
from uuid import UUID


class JobRunNotFoundError(HTTPException):
    def __init__(self, job_id: UUID, run_id: UUID):
        super().__init__(
            status_code=404,
            detail=f"Job run with ID {run_id} not found for job {job_id}."
        )
