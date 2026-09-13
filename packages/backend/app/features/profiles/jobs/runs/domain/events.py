from pydantic import BaseModel
from uuid import UUID


class RunCreatedEvent(BaseModel):
    run_id: UUID
    job_id: UUID
    version: int

    @property
    def routing_key(self) -> str:
        return "runs.created"


class RunFinishedEvent(BaseModel):
    run_id: UUID
    job_id: UUID
    model_id: UUID

    @property
    def routing_key(self) -> str:
        return "runs.finished"
