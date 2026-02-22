from __future__ import annotations

from abc import abstractmethod
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

from core.tasks.event import AbstractTaskEvent
from core.tasks.retry import RetryPolicy
from core.tasks.types import TaskType


class TaskEnvelope[T: BaseModel](AbstractTaskEvent):
    deduplication_key: Optional[str] = Field(
        None, description="Key used for deduplication of tasks")

    schema_version: int = Field(default=1, ge=1)

    payload: T = Field(...,
                       description="Payload containing the task-specific data")

    correlation_id: Optional[UUID] = Field(
        None, description="Correlation ID for tracing the task across services")

    attempt: int = Field(
        default=1, ge=1, description="Current attempt number for the task")

    retry_policy: Optional[RetryPolicy] = Field(None,
                                                description="Retry policy for the task")

    model_config = {
        "from_attributes": True,
    }

    @classmethod
    @abstractmethod
    def create(cls, payload: T,
               deduplication_key: Optional[str] = None,
               correlation_id: Optional[UUID] = None) -> TaskEnvelope[T]: ...

    @classmethod
    def create_unknown(
        cls,
        id: UUID,
        task_type: TaskType,
        payload: T,
        deduplication_key: Optional[str] = None,
        correlation_id: Optional[UUID] = None,
        retry_policy: Optional[RetryPolicy] = None
    ):
        return cls(
            task_id=id,
            task_type=task_type,
            payload=payload,
            deduplication_key=deduplication_key,
            correlation_id=correlation_id,
            retry_policy=retry_policy
        )
