from uuid import UUID
from pydantic import BaseModel


class CreateJobRun(BaseModel):
    job_id: UUID
