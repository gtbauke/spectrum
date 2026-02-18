from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from uuid import uuid4
from datetime import datetime
from pydantic import Field

from core.models.base import BaseDomainModel
from core.models.datasets.dataset_status import DatasetStatus

if TYPE_CHECKING:
    from core.models.datasets.dataset_metadata import DatasetMetadata
    from core.models.models.model import Model


class Dataset(BaseDomainModel):
    name: str = Field(..., description="The name of the dataset")

    status: DatasetStatus = Field(..., description="The status of the dataset")

    file_path: Optional[str] = Field(
        None, description="The file path of the dataset, if available"
    )

    checksum: str = Field(
        ..., description="The checksum of the dataset, if available"
    )

    dataset_metadata: Optional["DatasetMetadata"] = Field(
        None, description="The metadata of the dataset, if available"
    )

    models: list["Model"] = Field(
        [], description="The list of models associated with the dataset"
    )

    @classmethod
    def start_upload(cls, *, name: str, checksum: str) -> Dataset:
        return cls(
            id=uuid4(),
            name=name,
            status=DatasetStatus.PENDING,
            file_path=None,
            checksum=checksum,
            dataset_metadata=None,
            models=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def is_ready_for_model_training(self) -> bool:
        return self.status == DatasetStatus.COMPLETED
