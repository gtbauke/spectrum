from core.common.repositories.base.mutable import IMutableRepository

from core.features.profiles.jobs.job import Job
from core.features.profiles.jobs.where import JobWhere, JobFilter


class IJobsRepository(IMutableRepository[Job, JobWhere, JobFilter]):
    pass
