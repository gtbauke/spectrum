from typing import Protocol, BinaryIO
from .upload_result import UploadResult


class FileStorage(Protocol):
    async def upload(
        self,
        *,
        path: str,
        file: BinaryIO,
    ) -> UploadResult: ...
