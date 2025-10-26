import asyncio
import os
import time

from app.services.engines.storage.local_storage_engine import LocalStorageEngine


class TemporaryStorageEngine(LocalStorageEngine):
    def __init__(self, base_dir: str | None = None, ttl_seconds: int = 3600, cleanup_interval: int = 300):
        super().__init__(base_dir)
        self.ttl_seconds = ttl_seconds
        self.cleanup_interval = cleanup_interval

        if cleanup_interval > 0:
            asyncio.create_task(self.cleanup_task())

    async def cleanup_task(self):
        while True:
            await asyncio.sleep(self.cleanup_interval)
            await self.cleanup_expired_files()

    async def cleanup_expired_files(self):
        os.makedirs(self.base_dir, exist_ok=True)

        now = time.time()
        for file_name in os.listdir(self.base_dir):
            path = self.base_dir / file_name
            try:
                if os.path.isfile(path):
                    mtime = os.path.getmtime(path)
                    if now - mtime > self.ttl_seconds:
                        os.remove(path)
            except FileNotFoundError:
                continue
