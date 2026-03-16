from typing import Union

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.features.profiles.blocks.dto.create_block import InferenceBlock, MarkdownBlock
from core.models.profiles.profile_block import ProfileBlock
from core.models.profiles.profile_block_type import ProfileBlockType


class ProfileBlockDetails(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    order_index: int
    type: ProfileBlockType
    data: Union[
        MarkdownBlock,
        InferenceBlock,
    ]

    @classmethod
    def from_profile_block(cls, block: ProfileBlock):
        if block.type == ProfileBlockType.MARKDOWN:
            validated_data = MarkdownBlock.model_validate(block.data)
        elif block.type == ProfileBlockType.INFERENCE:
            validated_data = InferenceBlock.model_validate(block.data)
        else:
            raise ValueError(f"Unsupported block type: {block.type}")

        return cls(
            id=block.id,
            created_at=block.created_at,
            updated_at=block.updated_at,
            order_index=block.order_index,
            type=block.type,
            data=validated_data,
        )
