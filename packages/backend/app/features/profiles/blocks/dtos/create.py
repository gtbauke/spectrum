from pydantic import BaseModel, Field
from typing import Annotated, Union

from core.features.profiles.blocks.block_kind import MarkdownBlock, InferenceBlock


class CreateBlockDto(BaseModel):
    order_index: int = Field(..., description="The order index of the block")
    data: Annotated[Union[MarkdownBlock, InferenceBlock],
                    Field(discriminator='kind')]
