from abc import ABC, abstractmethod

from core.models.datasets.dataset import Dataset
from core.repositories.base import BaseRepository


class DatasetsRepository(BaseRepository[Dataset], ABC):
    @abstractmethod
    async def create(self, *, name: str) -> Dataset: ...

    @abstractmethod
    async def add(self, obj: Dataset) -> Dataset: ...

    @abstractmethod
    async def save(self, dataset: Dataset) -> None: ...
