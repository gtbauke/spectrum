import shutil
import uuid
import aiofiles

from pathlib import Path
from typing import BinaryIO

from core.common.file_storage.transactional_file_storage import TransactionalFileStorage


class LocalTransactionalFileStorage(TransactionalFileStorage):
    def __init__(self, base_path: Path):
        self._base_path = base_path
        self._staging_path = base_path / ".staging" / str(uuid.uuid4())
        self._operations: list[tuple[Path, Path]] = []

    async def stage(self, *, content: BinaryIO, destination: str) -> str:
        final_path = self._base_path / destination
        staged_path = self._staging_path / destination

        staged_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(staged_path, 'wb') as f:
            while chunk := content.read(1024):
                await f.write(chunk)

        self._operations.append((staged_path, final_path))
        return destination

    async def stage_delete(self, *, file_path: str) -> None:
        final_path = self._base_path / file_path
        staged_path = self._staging_path / file_path

        if final_path.exists():
            staged_path.parent.mkdir(parents=True, exist_ok=True)
            final_path.rename(staged_path)
            self._operations.append((staged_path, final_path))
        else:
            # If the file doesn't exist, we can just ignore it or log a warning
            pass

    async def commit(self) -> None:
        for staged_path, final_path in self._operations:
            final_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(staged_path, final_path)

        shutil.rmtree(self._staging_path, ignore_errors=True)
        self._operations.clear()

    async def rollback(self) -> None:
        shutil.rmtree(self._staging_path, ignore_errors=True)
        self._operations.clear()
