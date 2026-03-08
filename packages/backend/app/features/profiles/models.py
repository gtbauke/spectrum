from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, Text, Enum, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, declared_attr, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from core.models.profiles.profile_status import ProfileStatus
from core.models.profiles.profile_visibility import ProfileVisibility
from core.models.profiles.profile_dataset_role import ProfileDatasetRole

from db.immutable import ImmutableBase

if TYPE_CHECKING:
    from app.features.datasets.models import DatasetVersionORM


class ProfileORM(ImmutableBase):
    __tablename__ = "profiles"

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[ProfileStatus] = mapped_column(
        Enum(ProfileStatus, name="profile_status"),
        nullable=False,
        default=ProfileStatus.ACTIVE,
    )

    visibility: Mapped[ProfileVisibility] = mapped_column(
        Enum(ProfileVisibility, name="profile_visibility"),
        nullable=False,
        default=ProfileVisibility.PRIVATE,
    )

    owner_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("owners.id", ondelete="CASCADE"),
        nullable=False,
    )

    dataset_versions: Mapped[list["DatasetVersionORM"]] = relationship(
        "DatasetVersionORM",
        secondary="profile_dataset_versions",
        back_populates="profiles",
        lazy="selectin"
    )

    @declared_attr.directive
    def __table_args__(cls):
        base_args = super().__table_args__ if hasattr(super(), "__table_args__") else ()

        return (
            *base_args,
            Index("ix_profiles_owner_id", "owner_id"),
            Index("ix_profiles_status", "status"),
            Index("ix_profiles_visibility", "visibility"),
            Index("ix_profiles_owner_visibility", "owner_id", "visibility")
        )


class ProfileDatasetVersionORM(ImmutableBase):
    __tablename__ = "profile_dataset_versions"

    profile_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    dataset_version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("dataset_versions.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    role: Mapped[ProfileDatasetRole] = mapped_column(
        Enum(ProfileDatasetRole, name="profile_dataset_role"),
        nullable=False,
    )

    @declared_attr.directive
    def __table_args__(cls):
        base_args = super().__table_args__ if hasattr(super(), "__table_args__") else ()

        return (
            *base_args,
            Index("ix_profile_dataset_versions_profile_id", "profile_id"),
            Index("ix_profile_dataset_versions_dataset_version_id",
                  "dataset_version_id"),
        )
