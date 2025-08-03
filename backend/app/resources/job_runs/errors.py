from fastapi import HTTPException
from app.utils.id import ID


class JobRunNotFoundError(HTTPException):
    def __init__(self, job_id: ID, run_id: ID):
        super().__init__(
            status_code=404,
            detail=f"Job run with ID {run_id} not found for job {job_id}."
        )
