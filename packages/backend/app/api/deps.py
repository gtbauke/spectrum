from app.db.uow.sqlalchemy import SqlAlchemyUnitOfWork

from db.session import AsyncSessionLocal
from core.ports.unit_of_work import UnitOfWork


def get_uow() -> UnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory=AsyncSessionLocal)
