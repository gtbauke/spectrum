from typing import Protocol, Iterable

from core.features.base import (
    BaseMutableDomainModel,
)

from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter

from .mutable import IMutableRepository


class IMutableBulkRepository[
    T_Mutable: BaseMutableDomainModel,
    T_Where: BaseUniqueWhere,
    T_Filter: BaseFilter,
](IMutableRepository[T_Mutable, T_Where, T_Filter], Protocol):
    async def add_many(self, entities: Iterable[T_Mutable]) -> None: ...
    async def update_many(self, entities: Iterable[T_Mutable]) -> None: ...
    async def delete_many(self, entities: Iterable[T_Mutable]) -> None: ...
