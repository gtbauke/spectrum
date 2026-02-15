from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class StartModelTrainingEvent(BaseModel):
    dataset_id: UUID
    model_id: Optional[UUID] = None

    def should_create_new_model(self) -> bool:
        return self.model_id is None
