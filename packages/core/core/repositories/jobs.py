from abc import abstractmethod

from core.models.jobs.job import Job
from core.models.jobs.where import JobFilter, JobWhere
from core.models.profiles.profile_version import ProfileVersion
from core.repositories.base import BaseVersionedRepository


class BaseJobsRepository(BaseVersionedRepository[
    Job,
    JobWhere,
    JobFilter,
]):
    @abstractmethod
    async def get_paginated(self, *, filter: JobFilter, limit: int = 20, offset: int = 0) -> tuple[list[Job], int]:
        ...

    @abstractmethod
    async def get_profile_version(self, *, where: JobWhere) -> ProfileVersion:
        ...
