from pydantic import BaseModel, Field

from app.domain.models.model import Model


class GetAllModelsResponse(BaseModel):
    models: list[Model] = Field(..., description="List of all trained models")
