from __future__ import annotations

from uuid import UUID
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from db.common.base.mutable import MutableBase


if TYPE_CHECKING:
    from db.features.profiles.model import ProfileORM
    from db.features.profiles.jobs.model import JobORM

class ModelORM(MutableBase):
    __tablename__ = "models"

    name: Mapped[str] = mapped_column(String, nullable=False)
    
    profile_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)
        
    generated_by: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)

    path: Mapped[str] = mapped_column(String, nullable=False)

    profile: Mapped["ProfileORM"] = relationship(
        "ProfileORM",
        back_populates="models",
        lazy="selectin",
        uselist=False,
    )

    job: Mapped["JobORM"] = relationship(
        "JobORM",
        back_populates="models",
        lazy="selectin",
        uselist=False,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None)
