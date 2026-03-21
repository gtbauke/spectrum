from uuid import UUID

from core.features.profiles.blocks.block_kind import BlockKind
from core.utils.filters.field_filter import (
    DateTimeFilter, EnumFilter, NumberFilter, UUIDFilter)
from core.utils.where import BaseUniqueWhere
from core.utils.filters.base import BaseFilter


class BlockWhere(BaseUniqueWhere):
    id: UUID


class BlockFilter(BaseFilter):
    id: UUIDFilter | None = None
    created_at: DateTimeFilter | None = None
    updated_at: DateTimeFilter | None = None
    profile_id: UUIDFilter | None = None
    order_index: NumberFilter[int] | None = None
    kind: EnumFilter[BlockKind] | None = None
