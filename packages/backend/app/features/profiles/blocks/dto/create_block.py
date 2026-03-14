from typing import Optional, Union
from pydantic import BaseModel

from app.features.profiles.models import ProfileBlockType, ProfileVisibility
from app.features.profiles.versions.dto.create_profile_version import CreateProfileVersionData
from core.models.profiles.profile_version import ProfileVersion


class BaseBlock(BaseModel):
    pass


class MetadataBlock(BaseBlock):
    name: str
    description: Optional[str] = None
    visibility: ProfileVisibility

    def build_from_diff(self, latest_version: ProfileVersion) -> CreateProfileVersionData:
        return CreateProfileVersionData(
            name=self.name,
            description=self.description if self.description is not None else latest_version.description,
            visibility=self.visibility
        )


class MarkdownBlock(BaseBlock):
    value: str


class InferenceBlock(BaseBlock):
    code: str


class CreateBlockDTO(BaseModel):
    type: ProfileBlockType
    data: Union[MarkdownBlock, InferenceBlock]
    order_index: int

    def get_json_data(self) -> dict:
        return self.data.model_dump()


class CreateBlocks(BaseModel):
    blocks: list[CreateBlockDTO]
    metadata_block: MetadataBlock
    # TODO: add datasets and jobs blocks
