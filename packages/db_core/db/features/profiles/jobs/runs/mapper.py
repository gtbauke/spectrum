from db.common.mappers.base import IMapper
from db.features.profiles.jobs.runs.model import RunORM

from core.features.profiles.jobs.runs.run import Run
from core.features.profiles.jobs.runs.status import JobRunStatus


class RunsMapper(IMapper[RunORM, Run]):
    @staticmethod
    def to_domain(orm: RunORM) -> Run:
        return Run(
            id=orm.id,
            version=orm.version,
            is_latest=orm.is_latest,
            timestamp=orm.timestamp,
            job_id=orm.job_id,
            status=JobRunStatus(orm.status),
            started_at=orm.started_at,
            finished_at=orm.finished_at,
        )

    @staticmethod
    def to_orm(domain: Run) -> RunORM:
        return RunORM(
            id=domain.id,
            version=domain.version,
            is_latest=domain.is_latest,
            timestamp=domain.timestamp,
            job_id=domain.job_id,
            status=domain.status.value,
            started_at=domain.started_at,
            finished_at=domain.finished_at,
        )
