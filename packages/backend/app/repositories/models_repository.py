from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.repositories.base import BaseRepository
from app.db.models.model import ModelORM
from app.domain.models.model import Model


class ModelsRepository(BaseRepository[ModelORM, Model], ABC):
    @abstractmethod
    async def get_by_dataset_id(self, dataset_id: UUID) -> ModelORM | None: ...

    @abstractmethod
    async def get_all_trained_models(self) -> Sequence[ModelORM]: ...

    @abstractmethod
    async def get_all_non_trained_models(self) -> Sequence[ModelORM]: ...
