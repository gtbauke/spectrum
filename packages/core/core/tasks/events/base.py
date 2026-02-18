from uuid import UUID
from pydantic import BaseModel, Field

from core.tasks.types import TaskType


class BaseTaskEvent(BaseModel):
    """
    Base class for task events, providing common fields and structure for all task-related events.
    """

    task_id: UUID = Field(
        ..., description="The unique identifier of the task associated with this event.")

    task_type: TaskType = Field(
        ..., description="The type of the task associated with this event.")
