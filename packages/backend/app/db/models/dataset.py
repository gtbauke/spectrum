from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from core.models.datasets.dataset import Dataset
from core.models.datasets.dataset_status import DatasetStatus

if TYPE_CHECKING:
    from app.db.models.model import ModelORM
    from app.db.models.job import JobORM
    from app.db.models.dataset_metadata import DatasetMetadataORM


class DatasetORM(Base):
    __tablename__ = "datasets"

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

    checksum: Mapped[str] = mapped_column(
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

    jobs: Mapped[list[JobORM]] = relationship(
        back_populates="dataset",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @classmethod
    def from_domain(cls, dataset: Dataset) -> DatasetORM:
        return cls(
            id=dataset.id,
            name=dataset.name,
            status=dataset.status,
            file_path=dataset.file_path,
            checksum=dataset.checksum,
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
            models=[self.model.to_domain()
                    for self.model in self.models] if self.models else [],
            dataset_metadata=self.dataset_metadata.to_domain() if self.dataset_metadata else None,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
