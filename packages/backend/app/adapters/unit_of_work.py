from pathlib import Path
from core.ports.unit_of_work import UnitOfWork
from db.adapters.unit_of_work import SqlAlchemyUnitOfWork

from core.adapters.storage.local_storage import LocalStorage
from core.adapters.storage.s3_storage import S3FileStorage

from .events.buffered_events_publisher import BufferedEventsPublisher
from ..core.config import settings


class ApiUnitOfWork(SqlAlchemyUnitOfWork):
    async def __aenter__(self) -> UnitOfWork:
        await super().__aenter__()

        if settings.STORAGE_TYPE == "s3":
            self.file_storage = S3FileStorage(
                bucket=settings.S3_BUCKET,
                region=settings.S3_REGION,
                access_key=settings.S3_ACCESS_KEY,
                secret_key=settings.S3_SECRET_KEY,
                endpoint_url=settings.S3_ENDPOINT_URL,
            )
        else:
            self.file_storage = LocalStorage(
                base_path=Path(settings.FILE_STORAGE_SPECTRUM_DATA_PATH),
                base_url=settings.STORAGE_BASE_URL,
            )

        self.events_publisher = BufferedEventsPublisher(self._broker)

        self.register(self.events_publisher)
        return self
