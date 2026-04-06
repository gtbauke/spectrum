from core.ports.unit_of_work import UnitOfWork
from db.adapters.unit_of_work import SqlAlchemyUnitOfWork

from core.ports.events.buffered_events_publisher import BufferedEventsPublisher
from .local_storage import WorkerLocalStorage


class WorkerUnitOfWork(SqlAlchemyUnitOfWork):
    async def __aenter__(self) -> UnitOfWork:
        await super().__aenter__()

        self.file_storage = WorkerLocalStorage()
        self.events_publisher = BufferedEventsPublisher(self._broker)

        self.register(self.events_publisher)
        return self
