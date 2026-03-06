from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, ForeignKey, Integer, Enum
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

    @classmethod
    def from_domain(cls, dataset: Dataset) -> DatasetORM:
        return cls(
            id=dataset.id,
            name=dataset.name,
            description=dataset.description,
            owner_id=dataset.owner_id,
            timestamp=dataset.timestamp
        )

    def to_domain(self) -> Dataset:
        return Dataset(
            id=self.id,
            name=self.name,
            description=self.description,
            owner_id=self.owner_id,
            timestamp=self.timestamp
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
    def from_domain(cls, dataset_version: DatasetVersion) -> DatasetVersionORM:
        return cls(
            id=dataset_version.id,
            dataset_id=dataset_version.dataset_id,
            row_count=dataset_version.row_count,
            column_count=dataset_version.column_count,
            version=dataset_version.version,
            timestamp=dataset_version.timestamp
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
    def from_domain(cls, dataset_artifact: DatasetArtifact) -> DatasetArtifactORM:
        return cls(
            id=dataset_artifact.id,
            dataset_version_id=dataset_artifact.dataset_version_id,
            artifact_type=dataset_artifact.artifact_type,
            file_path=dataset_artifact.file_path,
            size_in_bytes=dataset_artifact.size_in_bytes,
            checksum=dataset_artifact.checksum,
            timestamp=dataset_artifact.timestamp
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
