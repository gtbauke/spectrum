from pydantic import BaseModel, Field
from datetime import timedelta
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

    backoff_seconds: int = Field(
        default=5,
        ge=0,
        description="Number of seconds to wait before retrying"
    )

    backoff_multiplier: float = Field(
        default=2.0,
        ge=1.0,
        description="Multiplier for backoff time after each retry"
    )

    def get_backoff_time(self, attempt: int) -> timedelta:
        """
        Calculate the backoff time based on the attempt number.

        :param attempt: The current attempt number (starting from 1)
        :return: The calculated backoff time as a timedelta
        """
        if attempt < 1:
            raise ValueError(
                "Attempt number must be greater than or equal to 1")

        backoff_time = self.backoff_seconds * \
            (self.backoff_multiplier ** (attempt - 1))

        return timedelta(seconds=backoff_time)
