from fastapi import Form
from uuid import UUID
from typing import BinaryIO, Optional
from pydantic import BaseModel, Field

from core.models.owners.owner import Owner
from core.models.profiles.profile_dataset_role import ProfileDatasetRole
from core.models.profiles.profile_visibility import ProfileVisibility


class CreateProfileVersionWithProfileDTO(BaseModel):
    name: str = Field(..., max_length=255,
                      description="The name of the profile")

    description: Optional[str] = Field(
        None, description="A brief description of the profile")

    visibility: ProfileVisibility = Field(...,
                                          description="The visibility of the profile")


class CreateProfileDTO(BaseModel):
    owner: Owner
    version: Optional[CreateProfileVersionWithProfileDTO] = None


class CreateProfileRouteDTO(BaseModel):
    version: Optional[CreateProfileVersionWithProfileDTO] = None


class CreateProfileFromDatasetRoute(BaseModel):
    dataset_name: str = Field(..., description="Name of the dataset")

    dataset_description: Optional[str] = Field(
        None, description="Description of the dataset")

    dataset_role: ProfileDatasetRole = Field(
        ProfileDatasetRole.TRAINING,
        description="The role the dataset assumes in the profile"
    )

    @classmethod
    def as_form(
        cls,
        dataset_name: str = Form(...),
        dataset_description: Optional[str] = Form(None),
        dataset_role: ProfileDatasetRole = Form(...),
    ):
        return cls(
            dataset_name=dataset_name,
            dataset_description=dataset_description,
            dataset_role=dataset_role,
        )


class CreateProfileFromDataset:
    dataset_name: str
    dataset_description: Optional[str]
    dataset_role: ProfileDatasetRole
    owner: Owner
    file: BinaryIO

    def __init__(
        self,
        *,
        dataset_name: str,
        dataset_description: Optional[str] = None,
        owner: Owner,
        dataset_role: ProfileDatasetRole,
        file: BinaryIO,
    ):
        self.dataset_name = dataset_name
        self.dataset_description = dataset_description
        self.owner = owner
        self.file = file
        self.dataset_role = dataset_role
