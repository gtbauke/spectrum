from __future__ import annotations
import uuid

from datetime import datetime
from sqlalchemy import DateTime, String, Enum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.domain.datasets.dataset import Dataset
from app.domain.datasets.dataset_status import DatasetStatus
from app.domain.datasets.dataset_metadata import DatasetMetadata
from app.db.models.model import ModelORM


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

    checksum: Mapped[str | None] = mapped_column(
        String(),
        nullable=True,
    )

    models: Mapped[list["ModelORM"]] = relationship(
        back_populates="dataset",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    dataset_metadata: Mapped["DatasetMetadataORM"] = relationship(
        back_populates="dataset",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
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
            checksum=self.checksum,
            dataset_metadata=self.dataset_metadata.to_domain() if self.dataset_metadata else None,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class DatasetMetadataORM(Base):
    __tablename__ = "dataset_metadata"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    dataset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("datasets.id"),
        nullable=False,
        unique=True,
    )

    dataset: Mapped["DatasetORM"] = relationship(
        back_populates="dataset_metadata",
        lazy="joined",
        foreign_keys=[dataset_id],
    )

    num_rows: Mapped[int] = mapped_column(
        nullable=False,
    )

    num_features: Mapped[int] = mapped_column(
        nullable=False,
    )

    processing_attempts: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
    )

    last_processing_error: Mapped[str | None] = mapped_column(
        String(),
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
    def from_domain(cls, metadata: DatasetMetadata) -> DatasetMetadataORM:
        return cls(
            id=metadata.id,
            dataset_id=metadata.dataset_id,
            num_rows=metadata.num_rows,
            num_features=metadata.num_features,
            processing_attempts=metadata.processing_attempts,
            last_processing_error=metadata.last_processing_error,
            created_at=metadata.created_at,
            updated_at=metadata.updated_at,
        )

    def to_domain(self) -> DatasetMetadata:
        return DatasetMetadata(
            id=self.id,
            dataset_id=self.dataset_id,
            num_rows=self.num_rows,
            num_features=self.num_features,
            processing_attempts=self.processing_attempts,
            last_processing_error=self.last_processing_error,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
