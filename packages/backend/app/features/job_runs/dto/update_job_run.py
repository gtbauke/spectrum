from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from core.models.job_runs.job_run_status import JobRunStatus


class UpdateJobRun(BaseModel):
    job_run_status: Optional[JobRunStatus] = None

    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
