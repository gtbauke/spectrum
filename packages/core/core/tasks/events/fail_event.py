from pydantic import Field
from datetime import datetime

from core.tasks.failure import TaskFailureReason
from core.tasks.events.base import BaseTaskEvent


class TaskFailedEvent(BaseTaskEvent):
    """
    Event representing a task failure, containing information about the failure and the task.
    """
    reason: TaskFailureReason = Field(...,
                                      description="The reason for the task failure.")

    details: str = Field(...,
                         description="Detailed information about the task failure.")

    attempt: int = Field(..., ge=1,
                         description="The attempt number at which the task failed.")

    failed_at: datetime = Field(default_factory=datetime.now,
                                description="The timestamp when the task failure was recorded.")
