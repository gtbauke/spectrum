from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.owners.owner import Owner
from core.models.owners.owner_type import OwnerType

from db.base import ImmutableBase

if TYPE_CHECKING:
    from app.features.users.models import UserORM


class OwnerORM(ImmutableBase):
    __tablename__ = "owners"

    owner_type: Mapped[OwnerType] = mapped_column(
        Enum(OwnerType, name="owner_type"),
        nullable=False,
        default=OwnerType.USER,
    )

    user_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        unique=True,
    )

    user: Mapped[UserORM] = relationship(
        "UserORM", back_populates="owner", uselist=False)

    @classmethod
    def from_domain(cls, owner: Owner) -> OwnerORM:
        return cls(
            id=owner.id,
            owner_type=owner.owner_type,
            version=owner.version,
            user_id=owner.user_id,
            timestamp=owner.timestamp,
        )

    def to_domain(self) -> Owner:
        return Owner(
            id=self.id,
            owner_type=self.owner_type,
            version=self.version,
            timestamp=self.timestamp,
            user_id=self.user_id,
        )
