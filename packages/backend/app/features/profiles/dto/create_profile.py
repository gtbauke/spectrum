from fastapi import Form
from uuid import UUID
from typing import BinaryIO, Optional
from pydantic import BaseModel, Field

from core.models.profiles.profile_visibility import ProfileVisibility


class CreateProfileVersionWithProfileDTO(BaseModel):
    name: str = Field(..., max_length=255,
                      description="The name of the profile")

    description: Optional[str] = Field(
        None, description="A brief description of the profile")

    visibility: ProfileVisibility = Field(...,
                                          description="The visibility of the profile")


class CreateProfileDTO(BaseModel):
    owner_id: UUID
    version: Optional[CreateProfileVersionWithProfileDTO] = None


class CreateProfileRouteDTO(BaseModel):
    version: Optional[CreateProfileVersionWithProfileDTO] = None


class CreateProfileFromDatasetRoute(BaseModel):
    dataset_name: str = Field(..., description="Name of the dataset")

    dataset_description: Optional[str] = Field(
        None, description="Description of the dataset")

    @classmethod
    def as_form(
        cls,
        dataset_name: str = Form(...),
        dataset_description: Optional[str] = Form(None),
    ):
        return cls(dataset_name=dataset_name, dataset_description=dataset_description)


class CreateProfileFromDataset:
    dataset_name: str
    dataset_description: Optional[str]
    owner_id: UUID
    file: BinaryIO

    def __init__(
        self,
        *,
        dataset_name: str,
        dataset_description: Optional[str] = None,
        owner_id: UUID,
        file: BinaryIO,
    ):
        self.dataset_name = dataset_name
        self.dataset_description = dataset_description
        self.owner_id = owner_id
        self.file = file
