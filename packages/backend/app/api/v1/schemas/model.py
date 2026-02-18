from pydantic import BaseModel, Field

from core.models.models.model import Model


class GetAllModelsResponse(BaseModel):
    models: list[Model] = Field(..., description="List of all trained models")
