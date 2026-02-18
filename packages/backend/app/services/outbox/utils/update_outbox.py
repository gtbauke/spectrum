from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from core.models.outbox.outbox_status import OutboxStatus


class UpdateOutboxData[Payload: BaseModel](BaseModel):
    """
    Data model for updating an outbox message.
    """
    status: OutboxStatus = Field(...,
                                 description="The status of the message in the outbox.")

    attempts: int = Field(...,
                          description="The number of attempts made to send the message.")

    last_error: Optional[str] = Field(
        None, description="The last error message encountered when trying to send the message, if any.")

    published_at: Optional[datetime] = Field(
        None, description="The timestamp when the message was successfully published, if applicable.")
