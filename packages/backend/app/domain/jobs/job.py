from __future__ import annotations

from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from datetime import datetime
from typing import TYPE_CHECKING

from app.domain.jobs.job_status import JobStatus

if TYPE_CHECKING:
    from app.domain.datasets.dataset import Dataset


class Job(BaseModel):
    id: UUID = Field(..., description="The unique identifier of the job")
    status: JobStatus = Field(
        JobStatus.PENDING, description="The current status of the job")
    dataset_id: UUID = Field(
        ..., description="The unique identifier of the dataset associated with the job")
    dataset: "Dataset" = Field(...,
                               description="The dataset associated with the job")
    created_at: datetime = Field(...,
                                 description="The creation timestamp of the job")
    started_at: datetime | None = Field(
        None, description="The timestamp when the job started, if it has started"
    )
    finished_at: datetime | None = Field(
        None, description="The timestamp when the job finished, if it has finished"
    )

    @classmethod
    def new(cls, dataset: "Dataset") -> Job:
        return cls(
            id=uuid4(),
            status=JobStatus.PENDING,
            dataset_id=dataset.id,
            dataset=dataset,
            created_at=datetime.now(),
            started_at=None,
            finished_at=None,
        )
