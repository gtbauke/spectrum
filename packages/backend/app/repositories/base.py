from typing import Optional, TypeVar, Generic
from abc import ABC, abstractmethod
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession


TypeORM = TypeVar("TypeORM")


class BaseRepository(ABC, Generic[TypeORM]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[TypeORM]: ...

    @abstractmethod
    async def get_for_update(self, id: UUID) -> Optional[TypeORM]: ...

    @abstractmethod
    async def add(self, obj: TypeORM) -> TypeORM: ...

    @abstractmethod
    async def update(self, obj: TypeORM) -> TypeORM: ...
