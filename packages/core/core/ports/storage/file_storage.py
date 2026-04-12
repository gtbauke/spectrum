from typing import Protocol, BinaryIO
from .upload_result import UploadResult


class FileStorage(Protocol):
    async def upload(
        self,
        *,
        path: str,
        file: BinaryIO,
    ) -> UploadResult: ...

    async def download(
        self,
        *,
        path: str,
        destination: str,
    ) -> None: ...

    async def generate_upload_url(
        self,
        *,
        path: str,
        expiration: int = 3600,
    ) -> str: ...

    async def generate_download_url(
        self,
        *,
        path: str,
        expiration: int = 3600,
    ) -> str: ...
