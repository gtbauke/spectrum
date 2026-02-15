from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class JobRun(BaseModel):
    id: UUID = Field(..., description="The unique identifier of the job run.")
    model_id: UUID = Field(...,
                           description="The model associated with the job run.")
    created_at: datetime = Field(...,
                                 description="The timestamp when the job run was created.")
    started_at: Optional[datetime] = Field(
        None, description="The timestamp when the job run started.")
    finished_at: Optional[datetime] = Field(
        None, description="The timestamp when the job run finished.")
