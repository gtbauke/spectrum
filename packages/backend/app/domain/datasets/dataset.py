from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from app.domain.datasets.dataset_status import DatasetStatus


class Dataset:
    def __init__(
        self,
        id: UUID,
        name: str,
        status: DatasetStatus,
        file_path: Optional[str],
        num_rows: Optional[int],
        num_features: Optional[int],
        processing_attempts: int,
        last_processing_error: Optional[str],
        checksum: Optional[str],
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.name = name
        self.status = status
        self.file_path = file_path
        self.num_rows = num_rows
        self.num_features = num_features
        self.processing_attempts = processing_attempts
        self.last_processing_error = last_processing_error
        self.checksum = checksum
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def start_upload(cls, *, name: str, checksum: str) -> Dataset:
        return cls(
            id=uuid4(),
            name=name,
            status=DatasetStatus.PENDING,
            file_path=None,
            num_rows=None,
            num_features=None,
            processing_attempts=0,
            last_processing_error=None,
            checksum=checksum,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def mark_processing(self) -> None:
        self.status = DatasetStatus.PROCESSING
        self.updated_at = datetime.now()

    def mark_completed(self) -> None:
        self.status = DatasetStatus.COMPLETED
        self.updated_at = datetime.now()

    def mark_failed(self, error: str) -> None:
        self.status = DatasetStatus.FAILED
        self.last_processing_error = error

        self.updated_at = datetime.now()
