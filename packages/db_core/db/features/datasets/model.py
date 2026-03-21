from __future__ import annotations

from uuid import UUID
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from core.features.datasets.artifact_role import ArtifactRole
from db.common.base.mutable import MutableBase
from db.common.base.immutable import ImmutableBase


if TYPE_CHECKING:
    from db.features.users.model import UserORM


class DatasetORM(MutableBase):
    __tablename__ = "datasets"

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

    owner_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    owner: Mapped["UserORM"] = relationship(
        "UserORM",
        back_populates="datasets",
        lazy="selectin"
    )

    artifacts: Mapped[list["ArtifactORM"]] = relationship(
        "ArtifactORM",
        back_populates="dataset",
        lazy="selectin"
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True)


class ArtifactORM(ImmutableBase):
    __tablename__ = "artifacts"

    dataset_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("datasets.id"),
        nullable=False
    )

    checksum: Mapped[str] = mapped_column(String, nullable=False)

    size_in_bytes: Mapped[int] = mapped_column(Integer, nullable=False)

    path: Mapped[str] = mapped_column(String, nullable=False)

    role: Mapped[ArtifactRole] = mapped_column(
        Enum(ArtifactRole), nullable=False)

    dataset: Mapped["DatasetORM"] = relationship(
        "DatasetORM",
        back_populates="artifacts",
        lazy="selectin"
    )
