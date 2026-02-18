from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

from core.tasks.types import TaskType


class AbstractTaskEvent(BaseModel):
    task_id: UUID = Field(..., description="Unique identifier of the task")

    task_type: TaskType = Field(..., description="Type of the task")

    timestamp: datetime = Field(default_factory=datetime.now,
                                description="Timestamp when the event occurred")

    model_config = {
        "from_attributes": True,
    }
