from pydantic import BaseModel, Field

from app.domain.models.model import Model
from app.domain.jobs.job import Job


class GetAllModelsResponse(BaseModel):
    models: list[Model] = Field(..., description="List of all trained models")


class GetModelResponse(Model):
    job: Job = Field(..., description="The job associated with the model")
