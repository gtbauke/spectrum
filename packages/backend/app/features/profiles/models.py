from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from core.models.profiles.profile_status import ProfileStatus
from core.models.profiles.profile_visibility import ProfileVisibility
from core.models.profiles.profile_dataset_role import ProfileDatasetRole

from db.immutable import ImmutableVersionedBase, ImmutableBase
from db.mutable import MutableBase

if TYPE_CHECKING:
    from app.features.datasets.models import DatasetVersionORM


class ProfileORM(MutableBase):
    __tablename__ = "profiles"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[ProfileStatus] = mapped_column(
        Enum(ProfileStatus), nullable=False)

    visibility: Mapped[ProfileVisibility] = mapped_column(
        Enum(ProfileVisibility), nullable=False)

    owner_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("owners.id"), nullable=False)

    versions: Mapped[list["ProfileVersionORM"]] = relationship(
        "ProfileVersionORM",
        back_populates="profile",
        cascade="all, delete-orphan",
        lazy="select"
    )


class ProfileVersionORM(ImmutableVersionedBase):
    __tablename__ = "profile_versions"

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
