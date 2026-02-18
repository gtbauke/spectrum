from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime

from core.tasks.base import TaskEnvelope
from core.tasks.types import TaskType


class ModelTrainTaskPayload(BaseModel):
    dataset_id: UUID = Field(...,
                             description="ID of the dataset to be used for training")

    model_id: Optional[UUID] = Field(
        None, description="Unique identifier for the model to be trained")

    def is_retraining_task(self) -> bool:
        return self.model_id is not None


class ModelTrainTask(TaskEnvelope[ModelTrainTaskPayload]):
    task_type: TaskType = Field(TaskType.MODEL_TRAINING,
                                description="Type of the background task")

    payload: ModelTrainTaskPayload = Field(..., description="Task payload")

    @classmethod
    def create(
        cls,
        payload: ModelTrainTaskPayload,
        deduplication_key: Optional[str] = None,
        correlation_id: Optional[UUID] = None
    ) -> TaskEnvelope[ModelTrainTaskPayload]:
        return cls(
            task_id=uuid4(),
            task_type=TaskType.MODEL_TRAINING,
            payload=payload,
            created_at=datetime.now(),
            deduplication_key=deduplication_key,
            correlation_id=correlation_id,
        )
