from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.db.models import DatasetORM


class DatasetsRepository(ABC):
    @abstractmethod
    async def get(self, dataset_id: UUID) -> Optional[DatasetORM]: ...

    @abstractmethod
    async def create(self, *, name: str) -> DatasetORM: ...

    @abstractmethod
    async def add(self, dataset: DatasetORM) -> DatasetORM: ...

    @abstractmethod
    async def update(self, dataset: DatasetORM) -> None: ...
