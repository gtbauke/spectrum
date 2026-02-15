from app.repositories.base import BaseRepository
from app.db.models.job_run import JobRunORM


class JobRunRepository(BaseRepository[JobRunORM]):
    pass
