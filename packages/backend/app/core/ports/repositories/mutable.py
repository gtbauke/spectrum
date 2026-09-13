from typing import Protocol

from app.core.domain.base import (
    BaseMutableDomainModel,
)

from app.core.utils.where import BaseUniqueWhere
from app.core.utils.filters.base import BaseFilter

from .immutable import IImmutableRepository


class IMutableRepository[
    T_Mutable: BaseMutableDomainModel,
    T_Where: BaseUniqueWhere,
    T_Filter: BaseFilter,
](IImmutableRepository[T_Mutable, T_Where, T_Filter], Protocol):
    async def update(self, entity: T_Mutable) -> None: ...
    async def delete(self, entity: T_Mutable) -> None: ...
