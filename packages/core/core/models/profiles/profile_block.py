from uuid import UUID
from pydantic import Field

from core.models.base import BaseMutableDomainModel
from core.models.profiles.profile_block_type import ProfileBlockType


class ProfileBlock(BaseMutableDomainModel):
    version_id: UUID = Field(...,
                             description="The ID of the profile version this block belongs to")

    order_index: int = Field(..., description="The order index of the block")

    type: ProfileBlockType = Field(..., description="The type of the block")

    data: dict = Field(..., description="The data of the block")

    @classmethod
    def new(
        cls,
        *,
        version_id: UUID,
        order_index: int,
        type: ProfileBlockType,
        data: dict
    ):
        return cls(
            version_id=version_id,
            order_index=order_index,
            type=type,
            data=data
        )
