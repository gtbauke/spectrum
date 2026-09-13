from uuid import UUID

from app.features.profiles.blocks.domain.block_kind import BlockKind
from app.core.utils.filters.field_filter import (
    DateTimeFilter, EnumFilter, NumberFilter, UUIDFilter)
from app.core.utils.where import BaseUniqueWhere
from app.core.utils.filters.base import BaseFilter


class BlockWhere(BaseUniqueWhere):
    id: UUID


class BlockFilter(BaseFilter):
    id: UUIDFilter | None = None
    created_at: DateTimeFilter | None = None
    updated_at: DateTimeFilter | None = None
    profile_id: UUIDFilter | None = None
    order_index: NumberFilter[int] | None = None
    kind: EnumFilter[BlockKind] | None = None
