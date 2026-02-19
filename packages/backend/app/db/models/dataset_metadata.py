from __future__ import annotations
from uuid import UUID
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from core.models.datasets.dataset_metadata import DatasetMetadata

if TYPE_CHECKING:
    from app.db.models.dataset import DatasetORM


class DatasetMetadataORM(Base):
    __tablename__ = "dataset_metadata"

    dataset_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("datasets.id"),
        nullable=False,
        unique=True,
    )

    dataset: Mapped["DatasetORM"] = relationship(
        back_populates="dataset_metadata",
        lazy="selectin",
        foreign_keys=[dataset_id],
    )

    num_rows: Mapped[Optional[int]] = mapped_column(
        nullable=True,
    )

    num_features: Mapped[Optional[int]] = mapped_column(
        nullable=True,
    )

    processing_attempts: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
    )

    last_processing_error: Mapped[Optional[str]] = mapped_column(
        String(),
        nullable=True,
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
