from typing import Optional
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from core.models.base import RootDomainModel
from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter
from core.utils.pagination.base import Pagination


class BaseRepository[
    DomainType: RootDomainModel,
    WhereType: BaseUniqueWhere,
    FilterType: BaseFilter,
](ABC):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    @abstractmethod
    async def get_unique(self, where: WhereType) -> Optional[DomainType]: ...

    @abstractmethod
    async def get_for_update(
        self, where: WhereType) -> Optional[DomainType]: ...

    @abstractmethod
    async def add(self, obj: DomainType,
                  commit: bool = True) -> DomainType: ...

    @abstractmethod
    async def update(self, obj: DomainType,
                     commit: bool = True) -> DomainType: ...

    @abstractmethod
    async def delete(self, where: WhereType) -> None: ...

    @abstractmethod
    async def list_all(self, where: Optional[FilterType] = None,
                       pagination: Optional[Pagination] = None) -> list[DomainType]: ...


class BaseVersionedRepository[
    DomainType: RootDomainModel,
    WhereType: BaseUniqueWhere,
    FilterType: BaseFilter,
](BaseRepository[DomainType, WhereType, FilterType]):
    @abstractmethod
    async def unset_latest(self, where: WhereType) -> Optional[DomainType]: ...

    @abstractmethod
    async def get_latest_version_number(self, where: WhereType) -> int: ...
