from pydantic import BaseModel
from uuid import UUID


class RunCreatedEvent(BaseModel):
    run_id: UUID
    job_id: UUID

    @property
    def routing_key(self) -> str:
        return "runs.created"
