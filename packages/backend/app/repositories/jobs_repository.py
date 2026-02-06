from app.repositories.base import BaseRepository
from app.db.models.job import JobORM


class JobsRepository(BaseRepository[JobORM]):
    pass
