from uuid import UUID
from pydantic import BaseModel


class StartModelTrainingEvent(BaseModel):
    model_id: UUID
    dataset_id: UUID
