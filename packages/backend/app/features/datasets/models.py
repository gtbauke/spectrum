from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from uuid import UUID
from datetime import datetime

from sqlalchemy import String, ForeignKey, Integer, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from db.base import TimestampBase, ImmutableBase

from core.models.datasets.dataset import Dataset
from core.models.datasets.dataset_version import DatasetVersion
from core.models.datasets.dataset_artifact import DatasetArtifact
from core.models.datasets.artifact_type import ArtifactType

if TYPE_CHECKING:
    from app.features.profiles.models import ProfileORM


class DatasetORM(TimestampBase):
    __tablename__ = "datasets"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True)

    owner_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("owners.id"),
        nullable=False
    )

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    @classmethod
    def from_domain(cls, domain_obj: Dataset) -> DatasetORM:
        return cls(
            id=domain_obj.id,
            name=domain_obj.name,
            description=domain_obj.description,
            owner_id=domain_obj.owner_id,
            timestamp=domain_obj.timestamp,
            deleted_at=domain_obj.deleted_at
        )

    def to_domain(self) -> Dataset:
        return Dataset(
            id=self.id,
            name=self.name,
            description=self.description,
            owner_id=self.owner_id,
            timestamp=self.timestamp,
            deleted_at=self.deleted_at
        )


class DatasetVersionORM(ImmutableBase):
    __tablename__ = "dataset_versions"

    dataset_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("datasets.id"),
        nullable=False
    )

    row_count: Mapped[int] = mapped_column(Integer, nullable=False)
    column_count: Mapped[int] = mapped_column(Integer, nullable=False)

    profiles: Mapped[list["ProfileORM"]] = relationship(
        "ProfileORM",
        secondary="profile_dataset_versions",
        back_populates="dataset_versions",
        lazy="selectin"
    )

    @classmethod
    def from_domain(cls, domain_obj: DatasetVersion) -> DatasetVersionORM:
        return cls(
            id=domain_obj.id,
            dataset_id=domain_obj.dataset_id,
            row_count=domain_obj.row_count,
            column_count=domain_obj.column_count,
            version=domain_obj.version,
            timestamp=domain_obj.timestamp
        )

    def to_domain(self) -> DatasetVersion:
        return DatasetVersion(
            id=self.id,
            dataset_id=self.dataset_id,
            row_count=self.row_count,
            column_count=self.column_count,
            version=self.version,
            timestamp=self.timestamp
        )


class DatasetArtifactORM(TimestampBase):
    __tablename__ = "dataset_artifacts"

    dataset_version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("dataset_versions.id"),
        nullable=False
    )

    artifact_type: Mapped[ArtifactType] = mapped_column(
        Enum(ArtifactType), nullable=False)

    file_path: Mapped[str] = mapped_column(String, nullable=False)
    size_in_bytes: Mapped[int] = mapped_column(Integer, nullable=False)

    checksum: Mapped[str] = mapped_column(String, nullable=False)

    @classmethod
    def from_domain(cls, domain_obj: DatasetArtifact) -> DatasetArtifactORM:
        return cls(
            id=domain_obj.id,
            dataset_version_id=domain_obj.dataset_version_id,
            artifact_type=domain_obj.artifact_type,
            file_path=domain_obj.file_path,
            size_in_bytes=domain_obj.size_in_bytes,
            checksum=domain_obj.checksum,
            timestamp=domain_obj.timestamp
        )

    def to_domain(self) -> DatasetArtifact:
        return DatasetArtifact(
            id=self.id,
            dataset_version_id=self.dataset_version_id,
            artifact_type=self.artifact_type,
            file_path=self.file_path,
            size_in_bytes=self.size_in_bytes,
            checksum=self.checksum,
            timestamp=self.timestamp
        )
