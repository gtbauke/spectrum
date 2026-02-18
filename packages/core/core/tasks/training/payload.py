from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class ModelTrainTaskPayload(BaseModel):
    dataset_id: UUID = Field(...,
                             description="ID of the dataset to be used for training")

    model_id: Optional[UUID] = Field(
        None, description="Unique identifier for the model to be trained")

    def is_retraining_task(self) -> bool:
        return self.model_id is not None
