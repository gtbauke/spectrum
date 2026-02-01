from __future__ import annotations
import uuid

from datetime import datetime
from sqlalchemy import DateTime, String, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.domain.datasets.dataset import Dataset
from app.domain.datasets.dataset_status import DatasetStatus


class DatasetORM(Base):
    __tablename__ = "datasets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        nullable=False,
    )

    status: Mapped[DatasetStatus] = mapped_column(
        Enum(
            DatasetStatus,
            name="dataset_status",
        ),
        nullable=False,
        default=DatasetStatus.PENDING,
    )

    file_path: Mapped[str | None] = mapped_column(
        String(),
        nullable=True,
    )

    num_rows: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    num_features: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )

    @classmethod
    def from_domain(cls, dataset: Dataset) -> DatasetORM:
        return cls(
            id=dataset.id,
            name=dataset.name,
            created_at=dataset.created_at,
            updated_at=dataset.updated_at,
        )

    def to_domain(self) -> Dataset:
        return Dataset(
            id=self.id,
            name=self.name,
            status=self.status,
            file_path=self.file_path,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
