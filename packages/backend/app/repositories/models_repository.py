from abc import ABC, abstractmethod
from uuid import UUID

from app.repositories.base import BaseRepository
from app.db.models.model import ModelORM
from app.domain.models.model import Model


class ModelsRepository(BaseRepository[ModelORM, Model], ABC):
    @abstractmethod
    async def get_by_dataset_id(self, dataset_id: UUID) -> ModelORM | None: ...
