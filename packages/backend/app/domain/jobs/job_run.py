from typing import Optional
from pydantic import Field
from uuid import UUID
from datetime import datetime

from app.domain.base import BaseDomainModel


class JobRun(BaseDomainModel):
    model_id: UUID = Field(...,
                           description="The model associated with the job run.")

    created_at: datetime = Field(...,
                                 description="The timestamp when the job run was created.")

    started_at: Optional[datetime] = Field(
        None, description="The timestamp when the job run started.")

    finished_at: Optional[datetime] = Field(
        None, description="The timestamp when the job run finished.")
