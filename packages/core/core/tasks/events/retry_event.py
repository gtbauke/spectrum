from pydantic import Field
from datetime import datetime

from core.tasks.events.base import BaseTaskEvent


class TaskRetryScheduledEvent(BaseTaskEvent):
    attempt: int = Field(..., ge=1,
                         description="The current attempt number for the task retry.")

    next_attempt_at: datetime = Field(
        ..., description="The scheduled time for the next retry attempt of the task.")
