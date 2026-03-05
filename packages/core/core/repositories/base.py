from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.base import RootDomainModel
from core.utils.where import BaseWhere


class BaseRepository[DomainType: RootDomainModel](ABC):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    @abstractmethod
    async def get_unique(self, where: BaseWhere) -> Optional[DomainType]: ...

    @abstractmethod
    async def get_for_update(self, id: UUID) -> Optional[DomainType]: ...

    @abstractmethod
    async def add(self, obj: DomainType) -> DomainType: ...

    @abstractmethod
    async def update(self, obj: DomainType) -> DomainType: ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...

    @abstractmethod
    async def list_all(
        self, where_id: Optional[UUID] = None) -> list[DomainType]: ...
