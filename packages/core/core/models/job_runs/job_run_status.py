from enum import StrEnum


class JobRunStatus(StrEnum):
    QUEUED = "queued"
    WAITING = "waiting"
    RUNNING = "running"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    KILLED = "killed"
    DELETED = "deleted"
