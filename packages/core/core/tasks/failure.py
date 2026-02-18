from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from core.tasks.types import TaskType


class TaskFailureReason(StrEnum):
    UNKNOWN_ERROR = "unknown_error"
    VALIDATION_ERROR = "validation_error"
    EXTERNAL_SERVICE_FAILURE = "external_service_failure"
    TIMEOUT = "timeout"
    DEPENDENCY_FAILURE = "dependency_failure"


class TaskFailure(BaseModel):
    task_id: UUID = Field(...,
                          description="Unique identifier of the failed task")

    task_type: TaskType = Field(..., description="Type of the failed task")

    attempt: int = Field(..., ge=1,
                         description="Attempt number at which the task failed")

    reason: TaskFailureReason = Field(...,
                                      description="Reason for task failure")

    details: str = Field(...,
                         description="Detailed information about the failure")

    failed_at: datetime = Field(default_factory=datetime.now,
                                description="Timestamp when the task failure was recorded")

    retryable: bool = Field(
        default=False, description="Indicates if the task failure is retryable")

    stacktrace: Optional[str] = Field(
        None, description="Stack trace of the failure, if available")
