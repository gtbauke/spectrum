from db.session import AsyncSessionLocal
from workers.infra.unit_of_work import WorkerUnitOfWork


def get_uow() -> WorkerUnitOfWork:
    return WorkerUnitOfWork(session_factory=AsyncSessionLocal)
