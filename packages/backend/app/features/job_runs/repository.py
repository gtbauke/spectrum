from core.models.job_runs.job_run import JobRun
from core.models.job_runs.where import JobRunFilter, JobRunWhere
from core.repositories.job_runs import BaseJobRunsRepository

from app.core.repository import BaseRepositoryImplementation
from app.features.job_runs.models import JobRunORM


class JobRunsRepository(BaseJobRunsRepository, BaseRepositoryImplementation[
    JobRun,
    JobRunORM,
    JobRunWhere,
    JobRunFilter,
]):
    orm_model = JobRunORM
