from __future__ import annotations

import uuid

from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import DateTime, String, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.domain.models.model import Model

if TYPE_CHECKING:
    from app.db.models.dataset import DatasetORM
    from app.db.models.job import JobORM


class ModelORM(Base):
    __tablename__ = "models"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    dataset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("datasets.id"),
        nullable=False,
    )

    dataset: Mapped["DatasetORM"] = relationship(
        back_populates="models",
    )

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    job: Mapped["JobORM"] = relationship(
        back_populates="model",
        lazy="selectin",
    )

    model_file: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )

    def to_domain(self) -> Model:
        return Model(
            id=self.id,
            name=self.name,
            dataset_id=self.dataset_id,
            model_file=self.model_file,
            created_at=self.created_at,
            updated_at=self.updated_at,
            job=self.job.to_domain() if self.job else None,
        )

    @classmethod
    def from_domain(cls, model: Model) -> ModelORM:
        return cls(
            id=model.id,
            name=model.name,
            dataset_id=model.dataset_id,
            model_file=model.model_file,
            created_at=model.created_at,
            updated_at=model.updated_at,
            job=model.job if model.job else None,
        )
