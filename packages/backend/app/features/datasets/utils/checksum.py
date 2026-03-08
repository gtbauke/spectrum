import hashlib
from typing import BinaryIO


async def checksum_and_size(file: BinaryIO) -> tuple[str, int]:
    hasher = hashlib.sha256()
    size = 0

    file.seek(0)

    while chunk := file.read(8192):
        hasher.update(chunk)
        size += len(chunk)

    return hasher.hexdigest(), size
