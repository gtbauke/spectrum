from __future__ import annotations

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.domain.jobs.job import Job


class Model(BaseModel):
    id: UUID

    name: str
    dataset_id: UUID
    job: Optional["Job"]

    model_file: Optional[str]

    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(cls, *, name: str, dataset_id: UUID, job: "Job", model_file: Optional[str] = None) -> Model:
        now = datetime.now()

        return cls(
            id=uuid4(),
            name=name,
            dataset_id=dataset_id,
            job=job,
            model_file=model_file,
            created_at=now,
            updated_at=now,
        )

    def has_model_artifacts(self) -> bool:
        return self.model_file is not None
