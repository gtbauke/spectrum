from typing import Optional
from uuid import UUID
from pydantic import Field

from core.models.outbox.aggregate_type import AggregateType
from core.utils.exactly_one_model import ExactlyOneModel


class OutboxSearchBy(ExactlyOneModel):
    """
    Model for searching outbox messages. This model ensures that only one of the fields is provided at a time.
    """
    id: Optional[UUID] = Field(
        None, description="The unique identifier of the outbox message.")

    aggregate_id: Optional[UUID] = Field(
        None, description="The unique identifier of the aggregate associated with the outbox message.")

    aggregate_type: Optional[AggregateType] = Field(
        None, description="The type of the aggregate associated with the outbox message.")

    # TODO: implement an actual resolver
    def resolve(self) -> UUID:
        if not self.id:
            raise ValueError("At least one field must be provided.")

        return self.id
