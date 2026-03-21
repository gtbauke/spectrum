from uuid import UUID
from pydantic import Field

from core.features.base import BaseMutableDomainModel

from .block_kind import BlockKind, BaseBlock


class Block(BaseMutableDomainModel):
    profile_id: UUID = Field(...,
                             description="The ID of the profile the block belongs to")

    kind: BlockKind = Field(..., description="The kind of the block")

    order_index: int = Field(..., description="The order index of the block")

    data: BaseBlock = Field(..., description="The data of the block")
