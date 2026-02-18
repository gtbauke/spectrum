from __future__ import annotations

from abc import abstractmethod
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

from core.tasks.retry import RetryPolicy
from core.tasks.types import TaskType


class TaskEnvelope[T: BaseModel](BaseModel):
    task_id: UUID = Field(...,
                          description="Unique identifier for the background task")

    task_type: TaskType = Field(..., description="Type of the background task")

    deduplication_key: Optional[str] = Field(
        None, description="Key used for deduplication of tasks")

    schema_version: int = Field(default=1, ge=1)
    payload: T = Field(...,
                       description="Payload containing the task-specific data")

    created_at: datetime = Field(...,
                                 description="Timestamp when the task was created")

    correlation_id: Optional[UUID] = Field(
        None, description="Correlation ID for tracing the task across services")

    attempt: int = Field(
        default=1, ge=1, description="Current attempt number for the task")
    retry_policy: Optional[RetryPolicy] = Field(None,
                                                description="Retry policy for the task")

    @classmethod
    @abstractmethod
    def create(cls, payload: T,
               deduplication_key: Optional[str] = None,
               correlation_id: Optional[UUID] = None) -> TaskEnvelope[T]: ...
