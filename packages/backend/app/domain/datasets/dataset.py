from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

from app.domain.datasets.dataset_status import DatasetStatus

if TYPE_CHECKING:
    from app.domain.datasets.dataset_metadata import DatasetMetadata
    from app.domain.jobs.job import Job


class Dataset(BaseModel):
    id: UUID = Field(..., description="The unique identifier of the dataset")
    name: str = Field(..., description="The name of the dataset")
    status: DatasetStatus = Field(..., description="The status of the dataset")
    file_path: Optional[str] = Field(
        None, description="The file path of the dataset, if available"
    )
    checksum: Optional[str] = Field(
        None, description="The checksum of the dataset, if available"
    )

    dataset_metadata: Optional["DatasetMetadata"] = Field(
        None, description="The metadata of the dataset, if available"
    )

    jobs: Optional[list["Job"]] = Field(
        [], description="The list of jobs associated with the dataset")

    created_at: datetime = Field(...,
                                 description="The creation timestamp of the dataset")
    updated_at: datetime = Field(...,
                                 description="The last update timestamp of the dataset")

    @classmethod
    def start_upload(cls, *, name: str, checksum: str) -> Dataset:
        return cls(
            id=uuid4(),
            name=name,
            status=DatasetStatus.PENDING,
            file_path=None,
            checksum=checksum,
            dataset_metadata=None,
            jobs=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def is_ready_for_model_training(self) -> bool:
        return self.status == DatasetStatus.COMPLETED
