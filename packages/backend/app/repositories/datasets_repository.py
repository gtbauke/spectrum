from abc import ABC, abstractmethod

from app.repositories.base import BaseRepository
from app.db.models import DatasetORM
from app.domain.datasets.dataset import Dataset


class DatasetsRepository(BaseRepository[DatasetORM, Dataset], ABC):
    @abstractmethod
    async def create(self, *, name: str) -> DatasetORM: ...

    @abstractmethod
    async def add(self, obj: DatasetORM) -> DatasetORM: ...

    @abstractmethod
    async def save(self, dataset: Dataset) -> None: ...

    @abstractmethod
    async def list(self) -> list[DatasetORM]: ...
