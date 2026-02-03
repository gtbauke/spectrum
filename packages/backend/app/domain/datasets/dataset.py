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
        checksum: Optional[str],
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.name = name
        self.status = status
        self.file_path = file_path
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
            checksum=checksum,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
