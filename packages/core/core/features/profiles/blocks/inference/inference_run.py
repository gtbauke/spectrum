from uuid import UUID
from pydantic import Field

from core.features.base import BaseImmutableVersionedDomainModel


class InferenceRun(BaseImmutableVersionedDomainModel):
    """
    Represents a single execution of an IQL script belonging to a profile block.
    """
    block_id: UUID = Field(...,
                           description="The ID of the block where the IQL was executed")
    profile_id: UUID = Field(...,
                             description="The ID of the profile where the execution happened")
    query: str = Field(..., description="The IQL query executed")

    @classmethod
    def new(cls, block_id: UUID, profile_id: UUID, query: str, version: int = 1):
        return cls(
            block_id=block_id,
            profile_id=profile_id,
            query=query,
            version=version,
            is_latest=True,
        )
