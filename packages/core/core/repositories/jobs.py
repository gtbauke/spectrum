from abc import abstractmethod

from core.models.jobs.job import Job
from core.models.jobs.job_version import JobVersion
from core.models.jobs.where import JobFilter, JobVersionFilter, JobVersionWhere, JobWhere
from core.models.profiles.profile_version import ProfileVersion
from core.repositories.base import BaseVersionedRepository, BaseRepository


class BaseJobsRepository(BaseRepository[
    Job,
    JobWhere,
    JobFilter,
]):
    @abstractmethod
    async def get_paginated(self, *, filter: JobFilter, limit: int = 20, offset: int = 0) -> tuple[list[Job], int]:
        ...


class BaseJobVersionsRepository(BaseVersionedRepository[
    JobVersion,
    JobVersionWhere,
    JobVersionFilter,
]):
    @abstractmethod
    async def get_paginated(self, *, filter: JobVersionFilter, limit: int = 20, offset: int = 0) -> tuple[list[JobVersion], int]:
        ...

    @abstractmethod
    async def get_profile_version(self, *, where: JobVersionWhere) -> ProfileVersion:
        ...
