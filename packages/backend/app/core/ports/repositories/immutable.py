from typing import Optional, Protocol, Sequence

from app.core.domain.base import (
    RootDomainModel,
)

from app.core.utils.where import BaseUniqueWhere
from app.core.utils.filters.base import BaseFilter
from app.core.utils.pagination.response import PaginatedResponse
from app.core.utils.pagination.base import Pagination


class IImmutableRepository[
    T_Immutable: RootDomainModel,
    T_Where: BaseUniqueWhere,
    T_Filter: BaseFilter,
](Protocol):
    async def add(self, entity: T_Immutable) -> None: ...
    async def get_unique(self, where: T_Where) -> Optional[T_Immutable]: ...

    async def list(self, filter: Optional[T_Filter] = None,
                   pagination: Optional[Pagination] = None) -> PaginatedResponse[T_Immutable]: ...

    async def list_all(
        self, filter: Optional[T_Filter] = None) -> Sequence[T_Immutable]: ...
