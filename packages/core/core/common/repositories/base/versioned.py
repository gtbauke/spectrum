from typing import Optional, Protocol
from uuid import UUID

from core.features.base import BaseImmutableVersionedDomainModel
from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter

from .immutable import IImmutableRepository


class IVersionedRepository[
    T_Versioned: BaseImmutableVersionedDomainModel,
    T_Where: BaseUniqueWhere,
    T_Filter: BaseFilter,
](IImmutableRepository[T_Versioned, T_Where, T_Filter], Protocol):
    async def get_latest_version(
        self, parent_id: UUID) -> Optional[T_Versioned]: ...

    async def get_version_by_number(
        self, parent_id: UUID, version: int) -> Optional[T_Versioned]: ...

    async def unset_latest_and_add(
        self, parent_id: UUID, new_entity: T_Versioned) -> None: ...
