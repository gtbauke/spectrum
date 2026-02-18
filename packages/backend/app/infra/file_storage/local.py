from __future__ import annotations

import aiofiles

from pathlib import Path
from typing import BinaryIO

from core.common.file_storage.base import AbstractFileStorage
from core.common.config import ROOT_PATH


class LocalFileStorage(AbstractFileStorage):
    def __init__(self, base_path: Path):
        self._base_path = base_path

    @classmethod
    def default(cls) -> LocalFileStorage:
        return cls(base_path=ROOT_PATH / "storage")

    async def save(self, *, content: BinaryIO, destination: str) -> str:
        full_path = self._base_path / destination
        full_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(full_path, mode="wb") as f:
            while chunk := content.read(1024):
                await f.write(chunk)

        return destination

    async def delete(self, *, file_path: str) -> None:
        full_path = self._base_path / file_path

        if full_path.exists():
            full_path.unlink()

    async def with_scope(self, scope: str) -> LocalFileStorage:
        return LocalFileStorage(base_path=self._base_path / scope)
