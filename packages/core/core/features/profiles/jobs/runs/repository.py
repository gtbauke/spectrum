from datetime import datetime

from core.common.repositories.base.versioned import IVersionedRepository

from core.features.profiles.jobs.runs.run import Run
from core.features.profiles.jobs.runs.status import JobRunStatus
from core.features.profiles.jobs.runs.where import RunWhere, RunFilter


class IRunsRepository(IVersionedRepository[Run, RunWhere, RunFilter]):
    async def update_status(
        self,
        *,
        where: RunWhere,
        status: JobRunStatus,
        started_at: datetime | None = None,
        finished_at: datetime | None = None,
    ) -> Run | None: ...
