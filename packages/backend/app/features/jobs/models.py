from __future__ import annotations
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, Float, Enum, ForeignKey, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from core.models.jobs.job import Job
from db.immutable import ImmutableVersionedBase
from db.mutable import MutableBase

from core.models.jobs.loss_function import LossFunction
from core.models.jobs.available_functions import AvailableFunction
from core.models.jobs.job_version import JobVersion
from core.models.job_runs.job_run import JobRun


if TYPE_CHECKING:
    from app.features.job_runs.models import JobRunORM


class JobORM(MutableBase):
    __tablename__ = "jobs"

    profile_version_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("profile_versions.id"),
        nullable=False,
    )

    owner_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("owners.id"),
        nullable=False,
    )

    versions: Mapped[list["JobVersionORM"]] = relationship(
        "JobVersionORM",
        back_populates="job"
    )

    runs: Mapped[list["JobRunORM"]] = relationship(
        "JobRunORM",
        back_populates="job"
    )

    @classmethod
    def from_domain(cls, domain_obj: Job) -> JobORM:
        return cls(
            id=domain_obj.id,
            created_at=domain_obj.created_at,
            updated_at=domain_obj.updated_at,
            profile_version_id=domain_obj.profile_version_id,
            owner_id=domain_obj.owner_id,
            versions=[
                JobVersionORM.from_domain(obj)
                for obj in domain_obj.versions
            ],
            runs=[
                JobRunORM.from_domain(obj)
                for obj in domain_obj.runs
            ]
        )

    def to_domain(self) -> Job:
        return Job(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            profile_version_id=self.profile_version_id,
            owner_id=self.owner_id,
            versions=[
                obj.to_domain()
                for obj in self.versions
            ],
            runs=[
                obj.to_domain()
                for obj in self.runs
            ]
        )


class JobVersionORM(ImmutableVersionedBase):
    __tablename__ = "job_versions"

    job_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("jobs.id"),
        nullable=False,
    )

    job: Mapped[JobORM] = relationship(
        "JobORM",
        back_populates="versions"
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    dataset_artifact_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("dataset_artifacts.id"),
        nullable=False,
    )

    generations: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    population: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    max_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    number_of_tournaments: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    crossover_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    mutation_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    non_terminals: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    loss: Mapped[LossFunction] = mapped_column(
        Enum(LossFunction),
        nullable=False,
    )

    optimization_iterations: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    optimization_repeats: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    max_param_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    split: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    simplify: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    @classmethod
    def from_domain(cls, domain_obj: JobVersion) -> JobVersionORM:
        return cls(
            name=domain_obj.name,
            job_id=domain_obj.job_id,
            dataset_artifact_id=domain_obj.dataset_artifact_id,
            generations=domain_obj.generations,
            population=domain_obj.population,
            max_size=domain_obj.max_size,
            number_of_tournaments=domain_obj.number_of_tournaments,
            crossover_probability=domain_obj.crossover_probability,
            mutation_probability=domain_obj.mutation_probability,
            non_terminals=AvailableFunction.from_list(
                *domain_obj.non_terminals),
            loss=domain_obj.loss,
            optimization_iterations=domain_obj.optimization_iterations,
            optimization_repeats=domain_obj.optimization_repeats,
            max_param_count=domain_obj.max_param_count,
            split=domain_obj.split,
            simplify=domain_obj.simplify,
            version=domain_obj.version,
            is_latest=domain_obj.is_latest,
            timestamp=domain_obj.timestamp,
            id=domain_obj.id,
        )

    def to_domain(self) -> JobVersion:
        return JobVersion(
            name=self.name,
            job_id=self.job_id,
            dataset_artifact_id=self.dataset_artifact_id,
            generations=self.generations,
            population=self.population,
            max_size=self.max_size,
            number_of_tournaments=self.number_of_tournaments,
            crossover_probability=self.crossover_probability,
            mutation_probability=self.mutation_probability,
            non_terminals=AvailableFunction.to_list(self.non_terminals),
            loss=self.loss,
            optimization_iterations=self.optimization_iterations,
            optimization_repeats=self.optimization_repeats,
            max_param_count=self.max_param_count,
            split=self.split,
            simplify=self.simplify,
            version=self.version,
            is_latest=self.is_latest,
            timestamp=self.timestamp,
            id=self.id,
        )
