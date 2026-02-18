from abc import ABC, abstractmethod
from uuid import UUID

from core.repositories.base import BaseRepository
from core.models.models.model import Model
from core.models.jobs.job import Job


class ModelsRepository(BaseRepository[Model], ABC):
    @abstractmethod
    async def get_by_dataset_id(self, dataset_id: UUID) -> Model | None: ...

    @abstractmethod
    async def get_with_job(
        self, model_id: UUID) -> tuple[Model, Job] | None: ...
