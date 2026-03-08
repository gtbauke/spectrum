from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from fastapi import Form


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
    owner_id: UUID = Field(...,
                           description="The ID of the user who owns the dataset")
