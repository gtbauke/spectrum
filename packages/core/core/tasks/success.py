from datetime import datetime
from pydantic import Field

from core.tasks.event import AbstractTaskEvent


class AbstractTaskSuccessEvent(AbstractTaskEvent):
    finished_at: datetime = Field(default_factory=datetime.now,
                                  description="Timestamp when the task finished successfully")
