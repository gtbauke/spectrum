import hashlib
import os
from pathlib import Path
from typing import BinaryIO, Optional

from core.ports.storage.file_storage import FileStorage
from core.ports.storage.path import SpectrumPath
from core.ports.storage.upload_result import UploadResult


class LocalStorage(FileStorage):
    def __init__(self, base_path: Path, base_url: Optional[str] = None) -> None:
        self._base_path = base_path.resolve()
        self._base_url = base_url

    async def upload(self, *, path: str, file: BinaryIO) -> UploadResult:
        full_path = (self._base_path / path).resolve()
        full_path.parent.mkdir(parents=True, exist_ok=True)

        hasher = hashlib.sha256()
        size = 0

        # Ensure we are at the beginning of the file
        file.seek(0)

        with open(full_path, "wb") as f:
            while chunk := file.read(8192):
                f.write(chunk)
                hasher.update(chunk)
                size += len(chunk)

        spectrum_path = SpectrumPath(full_path=full_path, path=Path(path))
        checksum = hasher.hexdigest()

        return UploadResult(path=spectrum_path, size=size, checksum=checksum)

    async def download(self, *, path: str, destination: str) -> None:
        source_path = (self._base_path / path).resolve()
        destination_path = Path(destination).resolve()

        if not source_path.exists():
            raise FileNotFoundError(f"File not found at path: {source_path}")

        destination_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Using a simple synchronous read/write for local files as requested
        # to match existing implementation logic and avoid blocking loop issues
        # although ideally this would be chunked or use a-io-files if necessary.
        destination_path.write_bytes(source_path.read_bytes())

    async def generate_upload_url(
        self,
        *,
        path: str,
        expiration: int = 3600,
    ) -> str:
        """
        LocalStorage does not support direct URL uploads in mock mode.
        """
        raise NotImplementedError("Direct URL upload is not supported in LocalStorage.")

    async def generate_download_url(
        self,
        *,
        path: str,
        expiration: int = 3600,
    ) -> str:
        if not self._base_url:
            raise ValueError("STORAGE_BASE_URL is not configured.")
        
        # Ensure base_url doesn't end with slash and path doesn't start with slash
        base_url = self._base_url.rstrip("/")
        normalized_path = path.lstrip("/")
        
        return f"{base_url}/download/{normalized_path}"
