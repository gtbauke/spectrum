from core.common.repositories.base.versioned import IVersionedRepository

from core.features.profiles.jobs.runs.run import Run
from core.features.profiles.jobs.runs.where import RunWhere, RunFilter


class IRunsRepository(IVersionedRepository[Run, RunWhere, RunFilter]):
    pass
