from __future__ import annotations

from uuid import UUID
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.core.database.base.mutable import MutableBase
from app.features.profiles.domain.profile_mode import ProfileMode

if TYPE_CHECKING:
    from app.features.users.model import UserORM
    from app.features.datasets.model import DatasetORM
    from app.features.profiles.jobs.model import JobORM
    from app.features.profiles.blocks.model import BlockORM
    from app.features.profiles.models.model import ModelORM


class ProfileORM(MutableBase):
    __tablename__ = "profiles"

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

    owner_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    owner: Mapped["UserORM"] = relationship(
        "UserORM",
        back_populates="profiles",
        lazy="selectin",
        uselist=False,
    )

    mode: Mapped[ProfileMode] = mapped_column(
        Enum(ProfileMode), nullable=False, default=ProfileMode.DRAFT)

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None)

    datasets: Mapped[list["DatasetORM"]] = relationship(
        "DatasetORM",
        secondary="profiles_datasets",
        back_populates="profiles",
        lazy="selectin",
        order_by="DatasetORM.created_at",
    )

    jobs: Mapped[list["JobORM"]] = relationship(
        "JobORM",
        back_populates="profile",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="JobORM.created_at",
    )

    blocks: Mapped[list["BlockORM"]] = relationship(
        "BlockORM",
        back_populates="profile",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="BlockORM.created_at",
    )

    models: Mapped[list["ModelORM"]] = relationship(
        "ModelORM",
        back_populates="profile",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="ModelORM.created_at",
    )
