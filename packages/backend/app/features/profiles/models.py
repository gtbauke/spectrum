from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from core.models.profiles.profile_status import ProfileStatus
from core.models.profiles.profile_visibility import ProfileVisibility

from db.base import ImmutableBase

if TYPE_CHECKING:
    from ..users.models import UserORM


class Profile(ImmutableBase):
    __tablename__ = "profiles"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    dataset_file_path: Mapped[str] = mapped_column(String, nullable=True)

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

    # Relationships
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    user: Mapped["UserORM"] = relationship(
        "UserORM", back_populates="profiles")
