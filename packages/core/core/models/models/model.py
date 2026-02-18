from __future__ import annotations

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from pydantic import Field

from core.models.base import BaseDomainModel

if TYPE_CHECKING:
    from core.models.jobs.job import Job


class Model(BaseDomainModel):
    name: str = Field(..., description="The name of the model.")

    dataset_id: UUID = Field(
        ..., description="The unique identifier of the dataset associated with the model.")

    job: Optional["Job"] = Field(
        None, description="The job associated with the model.")

    model_file: Optional[str] = Field(
        None, description="The file path to the model artifacts, if available."
    )

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
