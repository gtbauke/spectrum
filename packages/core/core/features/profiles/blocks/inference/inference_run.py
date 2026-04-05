from uuid import UUID
from enum import Enum
from typing import Optional
from pydantic import Field

from core.features.base import BaseImmutableVersionedDomainModel


class InferenceRunStatus(str, Enum):
    """
    Possible states of an inference execution run.
    """
    PENDING = "pending"
    RESOLVING_MODELS = "resolving_models"
    DOWNLOADING_DATA = "downloading_data"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"


class InferenceRun(BaseImmutableVersionedDomainModel):
    """
    Represents a single execution of an IQL script belonging to a profile block.
    """
    block_id: UUID = Field(...,
                           description="The ID of the block where the IQL was executed")
    profile_id: UUID = Field(...,
                             description="The ID of the profile where the execution happened")
    query: str = Field(..., description="The IQL query executed")

    status: InferenceRunStatus = Field(
        InferenceRunStatus.PENDING, description="Current execution status")
    execution_time_ms: Optional[int] = Field(
        None, description="Total time taken to execute the query in milliseconds")
    error: Optional[str] = Field(
        None, description="Error message if the run failed")

    @classmethod
    def new(cls, block_id: UUID, profile_id: UUID, query: str, version: int = 1):
        return cls(
            block_id=block_id,
            profile_id=profile_id,
            query=query,
            version=version,
            is_latest=True,
            status=InferenceRunStatus.PENDING,
            execution_time_ms=None,
            error=None
        )
