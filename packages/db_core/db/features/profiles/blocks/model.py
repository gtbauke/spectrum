from __future__ import annotations
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    Enum,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.dialects.postgresql import JSONB

from db.common.base.mutable import MutableBase
from core.features.profiles.blocks.block_kind import BlockKind


if TYPE_CHECKING:
    from db.features.profiles.model import ProfileORM


class BlockORM(MutableBase):
    __tablename__ = "blocks"

    profile_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("profiles.id"),
        nullable=False,
    )

    profile: Mapped["ProfileORM"] = relationship(
        "ProfileORM",
        back_populates="blocks",
        lazy="selectin"
    )

    kind: Mapped[BlockKind] = mapped_column(
        Enum(BlockKind),
        nullable=False,
    )

    order_index: Mapped[int] = mapped_column(
        nullable=False,
    )

    data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )
