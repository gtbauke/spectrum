from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from uuid import UUID
from datetime import datetime

from sqlalchemy import String, ForeignKey, Integer, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from db.immutable import ImmutableBase, ImmutableVersionedBase
from db.mutable import MutableBase

from core.models.datasets.dataset import Dataset
from core.models.datasets.dataset_version import DatasetVersion
from core.models.datasets.dataset_artifact import DatasetArtifact
from core.models.datasets.dataset_artifact_version import DatasetArtifactVersion
from core.models.datasets.artifact_type import ArtifactType

if TYPE_CHECKING:
    from app.features.profiles.models import ProfileORM


class DatasetORM(MutableBase):
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

    versions: Mapped[list["DatasetVersionORM"]] = relationship(
        "DatasetVersionORM",
        back_populates="dataset",
        lazy="select",
        cascade="all, delete-orphan"
    )

    @classmethod
    def from_domain(cls, domain_obj: Dataset) -> DatasetORM:
        return cls(
            id=domain_obj.id,
            name=domain_obj.name,
            description=domain_obj.description,
            owner_id=domain_obj.owner_id,
            deleted_at=domain_obj.deleted_at,
            created_at=domain_obj.created_at,
            updated_at=domain_obj.updated_at,
            versions=[DatasetVersionORM.from_domain(
                version) for version in domain_obj.versions]
        )

    def to_domain(self) -> Dataset:
        return Dataset(
            id=self.id,
            name=self.name,
            description=self.description,
            owner_id=self.owner_id,
            deleted_at=self.deleted_at,
            created_at=self.created_at,
            updated_at=self.updated_at,
            versions=[version.to_domain() for version in self.versions]
        )


class DatasetVersionORM(ImmutableVersionedBase):
    __tablename__ = "dataset_versions"

    dataset_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("datasets.id"),
        nullable=False
    )

    profiles: Mapped[list["ProfileORM"]] = relationship(
        "ProfileORM",
        secondary="profile_dataset_versions",
        back_populates="dataset_versions",
        lazy="selectin"
    )

    dataset: Mapped["DatasetORM"] = relationship(
        "DatasetORM",
        back_populates="versions",
        lazy="selectin"
    )

    artifacts: Mapped[list["DatasetVersionArtifactAssociationORM"]] = relationship(
        "DatasetVersionArtifactAssociationORM",
        back_populates="dataset_version",
        lazy="selectin",
    )

    @classmethod
    def from_domain(cls, domain_obj: DatasetVersion) -> DatasetVersionORM:
        return cls(
            id=domain_obj.id,
            dataset_id=domain_obj.dataset_id,
            version=domain_obj.version,
            timestamp=domain_obj.timestamp,
            is_latest=domain_obj.is_latest,
            artifacts=[DatasetVersionArtifactAssociationORM.from_domain(
                artifact) for artifact in domain_obj.artifacts]
        )

    def to_domain(self) -> DatasetVersion:
        return DatasetVersion(
            id=self.id,
            dataset_id=self.dataset_id,
            version=self.version,
            timestamp=self.timestamp,
            is_latest=self.is_latest,
            artifacts=[assoc.to_domain() for assoc in self.artifacts]
        )


class DatasetArtifactORM(ImmutableVersionedBase):
    __tablename__ = "dataset_artifacts"

    dataset_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("datasets.id"),
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(String, nullable=False)
    size_in_bytes: Mapped[int] = mapped_column(Integer, nullable=False)

    checksum: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    versions: Mapped[list["DatasetVersionArtifactAssociationORM"]] = relationship(
        "DatasetVersionArtifactAssociationORM",
        back_populates="dataset_artifact",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    @classmethod
    def from_domain(cls, domain_obj: DatasetArtifact) -> DatasetArtifactORM:
        return cls(
            id=domain_obj.id,
            dataset_id=domain_obj.dataset_id,
            file_path=domain_obj.file_path,
            size_in_bytes=domain_obj.size_in_bytes,
            checksum=domain_obj.checksum,
            timestamp=domain_obj.timestamp,
            version=domain_obj.version,
            is_latest=domain_obj.is_latest,
        )

    def to_domain(self) -> DatasetArtifact:
        return DatasetArtifact(
            id=self.id,
            dataset_id=self.dataset_id,
            file_path=self.file_path,
            size_in_bytes=self.size_in_bytes,
            checksum=self.checksum,
            timestamp=self.timestamp,
            version=self.version,
            is_latest=self.is_latest,
        )


class DatasetVersionArtifactAssociationORM(ImmutableBase):
    __tablename__ = "dataset_version_artifacts"

    dataset_version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("dataset_versions.id"),
        nullable=False
    )

    dataset_artifact_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("dataset_artifacts.id"),
        nullable=False
    )

    artifact_type: Mapped[ArtifactType] = mapped_column(
        Enum(ArtifactType), nullable=False)

    dataset_version: Mapped["DatasetVersionORM"] = relationship(
        "DatasetVersionORM",
        back_populates="artifacts",
        lazy="selectin"
    )

    dataset_artifact: Mapped["DatasetArtifactORM"] = relationship(
        "DatasetArtifactORM",
        back_populates="versions",
        lazy="selectin"
    )

    @classmethod
    def from_domain(cls, domain_obj: DatasetArtifactVersion) -> DatasetVersionArtifactAssociationORM:
        return cls(
            id=domain_obj.id,
            dataset_version_id=domain_obj.dataset_version_id,
            dataset_artifact_id=domain_obj.dataset_artifact_id,
            artifact_type=domain_obj.artifact_type,
            timestamp=domain_obj.timestamp,
        )

    def to_domain(self) -> DatasetArtifactVersion:
        return DatasetArtifactVersion(
            id=self.id,
            dataset_version_id=self.dataset_version_id,
            dataset_artifact_id=self.dataset_artifact_id,
            artifact_type=self.artifact_type,
            timestamp=self.timestamp,
        )
