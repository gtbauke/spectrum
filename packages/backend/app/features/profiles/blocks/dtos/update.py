from uuid import UUID
from pydantic import BaseModel, Field
from typing import Annotated, Union

from core.features.profiles.blocks.block_kind import MarkdownBlock, InferenceBlock


class UpdateBlockDto(BaseModel):
    order_index: int | None = Field(
        None, description="The order index of the block")
    data: Annotated[Union[MarkdownBlock, InferenceBlock],
                    Field(discriminator='kind')] | None = None


class BulkUpdateBlockDto(UpdateBlockDto):
    id: UUID = Field(..., description="The ID of the block to update")
