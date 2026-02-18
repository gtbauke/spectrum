from pydantic import Field
from typing import Optional
from datetime import datetime
from enum import StrEnum

from core.tasks.event import AbstractTaskEvent


class TaskFailureReason(StrEnum):
    UNKNOWN_ERROR = "unknown_error"
    VALIDATION_ERROR = "validation_error"
    EXTERNAL_SERVICE_FAILURE = "external_service_failure"
    TIMEOUT = "timeout"
    DEPENDENCY_FAILURE = "dependency_failure"


class AbstractTaskFailureEvent(AbstractTaskEvent):
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
