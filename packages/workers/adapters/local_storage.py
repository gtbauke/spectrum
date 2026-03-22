import hashlib

from typing import BinaryIO
from pathlib import Path

from core.common.config import Settings
from core.ports.storage.file_storage import FileStorage
from core.ports.storage.path import SpectrumPath
from core.ports.storage.upload_result import UploadResult


class WorkerLocalStorage(FileStorage):
    def __init__(self) -> None:
        settings = Settings()

        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent

        self._base_path = (project_root /
                           settings.FILE_STORAGE_SPECTRUM_DATA_PATH).resolve()

    async def upload(self, *, path: str, file: BinaryIO) -> UploadResult:
        full_path = self._base_path / path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        hasher = hashlib.sha256()
        size = 0

        file.seek(0)

        with open(full_path, "wb") as f:
            while chunk := file.read(8192):
                f.write(chunk)
                hasher.update(chunk)
                size += len(chunk)

        spectrum_path = SpectrumPath(full_path=full_path, path=Path(path))
        checksum = hasher.hexdigest()

        return UploadResult(path=spectrum_path, size=size, checksum=checksum)
