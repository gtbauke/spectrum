from __future__ import annotations

from typing import Optional
from pydantic import Field
from uuid import UUID, uuid4
from datetime import datetime

from core.models.base import BaseDomainModel


class JobRun(BaseDomainModel):
    model_id: UUID = Field(...,
                           description="The model associated with the job run.")

    created_at: datetime = Field(...,
                                 description="The timestamp when the job run was created.")

    started_at: Optional[datetime] = Field(
        None, description="The timestamp when the job run started.")

    finished_at: Optional[datetime] = Field(
        None, description="The timestamp when the job run finished.")

    @classmethod
    def create(cls, *, model_id: UUID, started_at: Optional[datetime], finished_at: Optional[datetime]) -> JobRun:
        now = datetime.now()

        return cls(
            id=uuid4(),
            model_id=model_id,
            created_at=now,
            updated_at=now,
            started_at=started_at,
            finished_at=finished_at,
        )
