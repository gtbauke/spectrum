from __future__ import annotations
from uuid import UUID
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from core.models.models.model import Model

if TYPE_CHECKING:
    from app.db.models.dataset import DatasetORM
    from app.db.models.job import JobORM


class ModelORM(Base):
    __tablename__ = "models"

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    dataset_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("datasets.id"),
        nullable=False,
    )

    dataset: Mapped["DatasetORM"] = relationship(
        back_populates="models",
    )

    job_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    job: Mapped["JobORM"] = relationship(
        back_populates="model",
        lazy="selectin",
    )

    model_file: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
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
