from uuid import UUID
from pydantic import BaseModel, Field


class InferenceRunRequestedEvent(BaseModel):
    """
    Event emitted when an IQL execution is requested.
    """
    run_id: UUID = Field(..., description="The ID of the run record")
    block_id: UUID = Field(...,
                           description="The ID of the block where the query is from")
    profile_id: UUID = Field(...,
                             description="The ID of the profile owning the block")
    query: str = Field(..., description="The IQL query to execute")

    @property
    def routing_key(self) -> str:
        return "inference.run_requested"
