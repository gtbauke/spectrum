from __future__ import annotations

from uuid import UUID
from typing import Any, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from db.immutable import ImmutableBase

from core.models.models.model import Model


class ModelORM(ImmutableBase):
    __tablename__ = "models"

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    model_path: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    profile_version_id: Mapped[UUID] = mapped_column(
        PG_UUID,
        ForeignKey("profile_versions.id"),
        nullable=False,
    )

    dataset_version_id: Mapped[UUID] = mapped_column(
        PG_UUID,
        ForeignKey("dataset_versions.id"),
        nullable=False,
    )

    dataset_artifact_id: Mapped[UUID] = mapped_column(
        PG_UUID,
        ForeignKey("dataset_artifacts.id"),
        nullable=False,
    )

    generated_by: Mapped[UUID] = mapped_column(
        PG_UUID,
        ForeignKey("jobs.id"),
        nullable=False,
    )

    owner: Mapped[UUID] = mapped_column(
        PG_UUID,
        ForeignKey("owners.id"),
        nullable=False,
    )

    @classmethod
    def from_domain(cls, domain_obj: Model) -> ModelORM:
        return cls(
            id=domain_obj.id,
            name=domain_obj.name,
            description=domain_obj.description,
            model_path=domain_obj.model_path,
            profile_version_id=domain_obj.profile_version_id,
            dataset_version_id=domain_obj.dataset_version_id,
            dataset_artifact_id=domain_obj.dataset_artifact_id,
            generated_by=domain_obj.generated_by,
            owner=domain_obj.owner,
            timestamp=domain_obj.timestamp,
        )

    def to_domain(self) -> Model:
        return Model(
            id=self.id,
            name=self.name,
            description=self.description,
            model_path=self.model_path,
            profile_version_id=self.profile_version_id,
            dataset_version_id=self.dataset_version_id,
            dataset_artifact_id=self.dataset_artifact_id,
            generated_by=self.generated_by,
            owner=self.owner,
            timestamp=self.timestamp,
        )
