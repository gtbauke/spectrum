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
