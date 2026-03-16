from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from fastapi import Form

from core.models.owners.owner import Owner


class CreateDatasetRouteDTO(BaseModel):
    name: str = Field(..., description="The name of the dataset")

    description: Optional[str] = Field(
        None, description="A description of the dataset")

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        description: Optional[str] = Form(None),
    ):
        return cls(name=name, description=description)


class CreateDatasetDTO(CreateDatasetRouteDTO):
    owner: Owner = Field(...,
                         description="The ID of the user who owns the dataset")
