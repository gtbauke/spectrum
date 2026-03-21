from abc import ABC, abstractmethod
from typing import Optional, Sequence
from pydantic import BaseModel

from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter
from core.utils.pagination.base import Pagination
from core.features.base import RootDomainModel
from core.ports.unit_of_work import UnitOfWork


class BaseService(ABC):
    """
    Base class for all services in the application. This class defines the interface that all services must implement. It also provides common functionality that can be shared across all services.
    """


class BaseCRUDService[
    ReturnType: RootDomainModel,
    WhereType: BaseUniqueWhere,
    CreateType: BaseModel,
    UpdateType: BaseModel,
    FilterType: BaseFilter,
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
    async def get_all(self, *, uow: UnitOfWork,
                      filter: Optional[FilterType] = None) -> Sequence[ReturnType]: ...


class BaseCRDService[
    ReturnType: RootDomainModel,
    WhereType: BaseUniqueWhere,
    CreateType: BaseModel,
    FilterType: BaseFilter,
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
    async def get_all(self, *, uow: UnitOfWork,
                      filter: Optional[FilterType] = None) -> Sequence[ReturnType]: ...


class BaseImmutableVersionedService[
    ReturnType: RootDomainModel,
    WhereType: BaseUniqueWhere,
    CreateType: BaseModel,
    UpdateType: BaseModel,
    FilterType: BaseFilter,
](BaseService):
    """
    Base class for all versioned entities in the application. This class defines the interface that all versioned entities must implement.
    """

    @abstractmethod
    async def get_unique(self, *, uow: UnitOfWork, where: WhereType) -> Optional[ReturnType]:
        ...

    @abstractmethod
    async def get_latest(self, *, uow: UnitOfWork, where: WhereType) -> Optional[ReturnType]:
        ...

    @abstractmethod
    async def create(self, *, uow: UnitOfWork, data: CreateType, version: int = 1) -> ReturnType:
        ...

    @abstractmethod
    async def create_new_version(self, *, uow: UnitOfWork, data: UpdateType, where: WhereType) -> ReturnType:
        ...

    @abstractmethod
    async def get_all(self, *, uow: UnitOfWork, filter: Optional[FilterType] = None,
                      pagination: Optional[Pagination] = None) -> Sequence[ReturnType]:
        ...
