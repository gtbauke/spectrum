from abc import ABC, abstractmethod
from typing import Optional, Sequence
from pydantic import BaseModel

from core.utils.where import BaseWhere
from core.models.base import RootDomainModel
from core.ports.unit_of_work import UnitOfWork


class BaseService(ABC):
    """
    Base class for all services in the application. This class defines the interface that all services must implement. It also provides common functionality that can be shared across all services.
    """


class BaseCRUDService[
    ReturnType: RootDomainModel,
    WhereType: BaseWhere,
    CreateType: BaseModel,
    UpdateType: BaseModel,
](BaseService):
    """
    Base class for all services in the application. This class defines the interface that all services must implement.
    It also provides common functionality that can be shared across all services.
    """

    @abstractmethod
    async def get_unique(
        self, *, uow: UnitOfWork, where: WhereType) -> Optional[ReturnType]: ...

    @abstractmethod
    async def create(self, *, uow: UnitOfWork,
                     data: CreateType) -> ReturnType: ...

    @abstractmethod
    async def update_unique(self, *, uow: UnitOfWork, where: WhereType,
                            data: UpdateType) -> ReturnType: ...

    @abstractmethod
    async def delete_unique(self, *, uow: UnitOfWork,
                            where: WhereType): ...

    @abstractmethod
    async def get_all(self, *, uow: UnitOfWork) -> Sequence[ReturnType]: ...


class BaseCRService[
    ReturnType: RootDomainModel,
    WhereType: BaseWhere,
    CreateType: BaseModel,
](BaseService):
    @abstractmethod
    async def get_unique(
        self, *, uow: UnitOfWork, where: WhereType) -> Optional[ReturnType]: ...

    @abstractmethod
    async def create(self, *, uow: UnitOfWork,
                     data: CreateType) -> ReturnType: ...

    @abstractmethod
    async def delete_unique(self, *, uow: UnitOfWork,
                            where: WhereType): ...

    @abstractmethod
    async def get_all(self, *, uow: UnitOfWork) -> Sequence[ReturnType]: ...
