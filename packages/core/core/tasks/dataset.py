from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

from core.tasks.base import TaskEnvelope
from core.tasks.retry import RetryPolicy
from core.tasks.types import TaskType


class DatasetProcessTaskPayload(BaseModel):
    dataset_id: UUID = Field(...,
                             description="The ID of the dataset to process")


class DatasetProcessTask(TaskEnvelope[DatasetProcessTaskPayload]):
    task_type: TaskType = Field(TaskType.DATASET_PROCESSING,
                                description="Type of the background task")

    payload: DatasetProcessTaskPayload = Field(..., description="Task payload")

    @classmethod
    def create(
        cls,
        payload: DatasetProcessTaskPayload,
        deduplication_key: Optional[str] = None,
        correlation_id: Optional[UUID] = None,
        retry_policy: Optional[RetryPolicy] = None
    ) -> TaskEnvelope[DatasetProcessTaskPayload]:
        return cls(
            task_id=uuid4(),
            task_type=TaskType.DATASET_PROCESSING,
            payload=payload,
            created_at=datetime.now(),
            deduplication_key=deduplication_key,
            correlation_id=correlation_id,
            retry_policy=retry_policy
        )
