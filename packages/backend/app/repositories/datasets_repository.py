from abc import ABC, abstractmethod

from app.repositories.base import BaseRepository
from app.db.models import DatasetORM
from core.models.datasets.dataset import Dataset

# TODO: clean up this class


class DatasetsRepository(BaseRepository[DatasetORM], ABC):
    @abstractmethod
    async def create(self, *, name: str) -> DatasetORM: ...

    @abstractmethod
    async def add(self, obj: DatasetORM) -> DatasetORM: ...

    @abstractmethod
    async def save(self, dataset: Dataset) -> None: ...
