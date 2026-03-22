from core.common.repositories.base.bulk import IMutableBulkRepository

from core.features.profiles.jobs.job import Job
from core.features.profiles.jobs.where import JobWhere, JobFilter


class IJobsRepository(IMutableBulkRepository[Job, JobWhere, JobFilter]):
    pass
