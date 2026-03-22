from core.ports.unit_of_work import UnitOfWork
from db.adapters.unit_of_work import SqlAlchemyUnitOfWork

from .storage.local_storage import LocalStorage


class ApiUnitOfWork(SqlAlchemyUnitOfWork):
    async def __aenter__(self) -> UnitOfWork:
        self.file_storage = LocalStorage()

        return await super().__aenter__()
