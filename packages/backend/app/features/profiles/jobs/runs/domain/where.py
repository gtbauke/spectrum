from uuid import UUID
from typing import TYPE_CHECKING

from app.core.utils.filters.field_filter import (
    BooleanFilter, DateTimeFilter, EnumFilter, NumberFilter, UUIDFilter)
from app.core.utils.where import BaseUniqueWhere
from app.core.utils.filters.base import BaseFilter

from .status import JobRunStatus

if TYPE_CHECKING:
    from app.features.profiles.jobs.domain.where import JobFilter


class RunWhere(BaseUniqueWhere):
    id: UUID | None = None
    job_id: UUID | None = None
    is_latest: bool | None = None
    version: int | None = None


class RunFilter(BaseFilter):
    id: UUIDFilter | None = None
    timestamp: DateTimeFilter | None = None
    version: NumberFilter[int] | None = None
    is_latest: BooleanFilter | None = None
    job_id: UUIDFilter | None = None
    status: EnumFilter[JobRunStatus] | None = None
    started_at: DateTimeFilter | None = None
    finished_at: DateTimeFilter | None = None
    job: "JobFilter | None" = None
