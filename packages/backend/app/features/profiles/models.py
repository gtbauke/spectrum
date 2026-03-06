from typing import Optional
from uuid import UUID

from sqlalchemy import String, Text, Enum, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, declared_attr
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from core.models.profiles.profile_status import ProfileStatus
from core.models.profiles.profile_visibility import ProfileVisibility

from db.base import ImmutableBase


class ProfileORM(ImmutableBase):
    __tablename__ = "profiles"

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    dataset_file_path: Mapped[Optional[str]
                              ] = mapped_column(String, nullable=True)

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
