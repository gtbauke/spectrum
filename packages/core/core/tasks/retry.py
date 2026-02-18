from pydantic import BaseModel, Field
from enum import StrEnum


class TaskRetryDecision(StrEnum):
    RETRY = "retry"
    FAIL = "fail"
    ACK = "ack"


class RetryPolicy(BaseModel):
    max_attempts: int = Field(
        default=3,
        ge=1,
        description="Maximum number of retry attempts"
    )
