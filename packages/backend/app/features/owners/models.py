from __future__ import annotations

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from core.models.owners.owner import Owner
from core.models.owners.owner_type import OwnerType

from db.base import ImmutableBase


class OwnerORM(ImmutableBase):
    __tablename__ = "owners"

    owner_type: Mapped[OwnerType] = mapped_column(
        Enum(OwnerType, name="owner_type"),
        nullable=False,
        default=OwnerType.USER,
    )

    @classmethod
    def from_domain(cls, owner: Owner) -> OwnerORM:
        return cls(
            id=owner.id,
            owner_type=owner.owner_type,
            version=owner.version,
            timestamp=owner.timestamp,
        )

    def to_domain(self) -> Owner:
        return Owner(
            id=self.id,
            owner_type=self.owner_type,
            version=self.version,
            timestamp=self.timestamp,
        )
