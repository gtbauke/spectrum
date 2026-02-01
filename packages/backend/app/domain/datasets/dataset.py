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
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.name = name
        self.status = status
        self.file_path = file_path
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def start_upload(cls, *, name: str) -> Dataset:
        return cls(
            id=uuid4(),
            name=name,
            status=DatasetStatus.PENDING,
            file_path=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def mark_processing(self, file_path: str) -> None:
        self.status = DatasetStatus.PROCESSING
        self.file_path = file_path

        self.updated_at = datetime.now()

    def mark_completed(self) -> None:
        self.status = DatasetStatus.COMPLETED
        self.updated_at = datetime.now()

    def mark_failed(self) -> None:
        self.status = DatasetStatus.FAILED
        self.updated_at = datetime.now()
