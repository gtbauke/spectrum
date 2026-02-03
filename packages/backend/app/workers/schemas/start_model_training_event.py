from uuid import UUID
from pydantic import BaseModel


class StartModelTrainingEvent(BaseModel):
    dataset_id: UUID
