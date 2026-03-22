from core.ports.unit_of_work import UnitOfWork
from db.adapters.unit_of_work import SqlAlchemyUnitOfWork

from .storage.local_storage import LocalStorage
from .events.buffered_events_publisher import BufferedEventsPublisher


class ApiUnitOfWork(SqlAlchemyUnitOfWork):
    async def __aenter__(self) -> UnitOfWork:
        await super().__aenter__()

        self.file_storage = LocalStorage()
        self.events_publisher = BufferedEventsPublisher(self._broker)

        self.register(self.events_publisher)
        return self
