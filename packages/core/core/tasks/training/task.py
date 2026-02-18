from pydantic import Field
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime

from core.tasks.base import TaskEnvelope
from core.tasks.retry import RetryPolicy
from core.tasks.training.payload import ModelTrainTaskPayload
from core.tasks.types import TaskType


TRAINING_RETRY_DELAYS = {
    1: 30_000,
    2: 120_000,
    3: 600_000,
    4: 1_800_000,
    5: 3_600_000,
}


class ModelTrainTask(TaskEnvelope[ModelTrainTaskPayload]):
    task_type: TaskType = Field(TaskType.MODEL_TRAINING,
                                description="Type of the background task")

    payload: ModelTrainTaskPayload = Field(..., description="Task payload")

    @classmethod
    def create(
        cls,
        payload: ModelTrainTaskPayload,
        deduplication_key: Optional[str] = None,
        correlation_id: Optional[UUID] = None,
        retry_policy: Optional[RetryPolicy] = None
    ) -> TaskEnvelope[ModelTrainTaskPayload]:
        return cls(
            task_id=uuid4(),
            task_type=TaskType.MODEL_TRAINING,
            payload=payload,
            timestamp=datetime.now(),
            deduplication_key=deduplication_key,
            correlation_id=correlation_id,
            retry_policy=retry_policy
        )
