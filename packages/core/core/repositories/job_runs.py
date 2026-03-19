from .base import BaseRepository

from core.models.job_runs.where import JobRunWhere, JobRunFilter
from core.models.job_runs.job_run import JobRun


class BaseJobRunsRepository(BaseRepository[JobRun, JobRunWhere, JobRunFilter]):
    pass
