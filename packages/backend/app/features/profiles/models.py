from __future__ import annotations

import logging

from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, Text, Enum, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from core.models.profiles.profile_block import ProfileBlock, ProfileBlockType
from core.models.profiles.profile_status import ProfileStatus
from core.models.profiles.profile_visibility import ProfileVisibility
from core.models.profiles.profile_dataset_role import ProfileDatasetRole
from core.models.profiles.profile import Profile
from core.models.profiles.profile_version import ProfileVersion
from core.models.profiles.profile_dataset_association import ProfileDatasetAssociation

from db.immutable import ImmutableVersionedBase, ImmutableBase
from db.mutable import MutableBase

if TYPE_CHECKING:
    from app.features.datasets.models import DatasetVersionORM
    from app.features.owners.models import OwnerORM
    from app.features.sr_models.models import ModelORM


logger = logging.getLogger(__name__)


class ProfileORM(MutableBase):
    __tablename__ = "profiles"

    owner_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("owners.id"), nullable=False)

    versions: Mapped[list["ProfileVersionORM"]] = relationship(
        "ProfileVersionORM",
        back_populates="profile",
        cascade="all, delete-orphan",
        lazy="select"
    )

    owner: Mapped["OwnerORM"] = relationship(
        "OwnerORM",
        lazy="selectin"
    )

    @classmethod
    def from_domain(cls, domain_obj: Profile) -> ProfileORM:
        return cls(
            id=domain_obj.id,
            owner_id=domain_obj.owner_id,
            created_at=domain_obj.created_at,
            updated_at=domain_obj.updated_at,
            versions=[
                ProfileVersionORM.from_domain(version)
                for version in domain_obj.versions
            ],
        )

    def to_domain(self) -> Profile:
        return Profile(
            id=self.id,
            owner_id=self.owner_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            versions=[version.to_domain() for version in self.versions],
            owner=self.owner.to_domain(),
        )


class ProfileVersionORM(ImmutableVersionedBase):
    __tablename__ = "profile_versions"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[ProfileStatus] = mapped_column(
        Enum(ProfileStatus), nullable=False)

    visibility: Mapped[ProfileVisibility] = mapped_column(
        Enum(ProfileVisibility), nullable=False)

    profile_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)

    profile: Mapped["ProfileORM"] = relationship(
        "ProfileORM",
        back_populates="versions",
    )

    datasets: Mapped[list["ProfileDatasetAssociationORM"]] = relationship(
        "ProfileDatasetAssociationORM",
        back_populates="profile_version",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    blocks: Mapped[list["ProfileBlockORM"]] = relationship(
        "ProfileBlockORM",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    models: Mapped[list["ModelORM"]] = relationship(
        "ModelORM",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @classmethod
    def from_domain(cls, domain_obj: ProfileVersion) -> ProfileVersionORM:
        return cls(
            id=domain_obj.id,
            version=domain_obj.version,
            is_latest=domain_obj.is_latest,
            timestamp=domain_obj.timestamp,
            name=domain_obj.name,
            description=domain_obj.description,
            status=domain_obj.status,
            visibility=domain_obj.visibility,
            profile_id=domain_obj.profile_id,
            datasets=[
                ProfileDatasetAssociationORM.from_domain(ds)
                for ds in domain_obj.datasets
            ],
            blocks=[
                ProfileBlockORM.from_domain(block)
                for block in domain_obj.blocks
            ],
            models=[
                ModelORM.from_domain(model)
                for model in domain_obj.models
            ],
        )

    def to_domain(self) -> ProfileVersion:
        return ProfileVersion(
            id=self.id,
            version=self.version,
            is_latest=self.is_latest,
            timestamp=self.timestamp,
            name=self.name,
            description=self.description,
            status=self.status,
            visibility=self.visibility,
            profile_id=self.profile_id,
            datasets=[ds.to_domain() for ds in self.datasets],
            blocks=[block.to_domain() for block in self.blocks],
            models=[model.to_domain() for model in self.models],
        )


class ProfileDatasetAssociationORM(ImmutableBase):
    __tablename__ = "profile_dataset_associations"

    profile_version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("profile_versions.id"),
        nullable=False,
    )

    dataset_version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("dataset_versions.id"),
        nullable=False,
    )

    role: Mapped[ProfileDatasetRole] = mapped_column(
        Enum(ProfileDatasetRole), nullable=False)

    dataset_version: Mapped["DatasetVersionORM"] = relationship(
        "DatasetVersionORM",
        back_populates="profile_associations",
        lazy="selectin"
    )

    profile_version: Mapped["ProfileVersionORM"] = relationship(
        "ProfileVersionORM",
        back_populates="datasets"
    )

    @classmethod
    def from_domain(cls, domain_obj: ProfileDatasetAssociation) -> ProfileDatasetAssociationORM:
        return cls(
            id=domain_obj.id,
            timestamp=domain_obj.timestamp,
            profile_version_id=domain_obj.profile_version_id,
            dataset_version_id=domain_obj.dataset_version_id,
            role=domain_obj.role,
        )

    def to_domain(self) -> ProfileDatasetAssociation:
        profile_dataset_association = ProfileDatasetAssociation(
            id=self.id,
            timestamp=self.timestamp,
            profile_version_id=self.profile_version_id,
            dataset_version_id=self.dataset_version_id,
            role=self.role,
            dataset_version=self.dataset_version.to_domain() if self.dataset_version else None,
        )

        return profile_dataset_association


class ProfileBlockORM(MutableBase):
    __tablename__ = "profile_blocks"

    version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("profile_versions.id"),
        nullable=False,
    )

    order_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    type: Mapped[ProfileBlockType] = mapped_column(
        Enum(ProfileBlockType),
        nullable=False,
    )

    data: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    @classmethod
    def from_domain(cls, domain_obj: ProfileBlock) -> ProfileBlockORM:
        return cls(
            id=domain_obj.id,
            version_id=domain_obj.version_id,
            order_index=domain_obj.order_index,
            type=domain_obj.type,
            data=domain_obj.data,
            created_at=domain_obj.created_at,
            updated_at=domain_obj.updated_at,
        )

    def to_domain(self) -> ProfileBlock:
        return ProfileBlock(
            id=self.id,
            version_id=self.version_id,
            order_index=self.order_index,
            type=self.type,
            data=self.data,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
