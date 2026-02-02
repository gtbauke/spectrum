import hashlib

from typing import BinaryIO
from fastapi import UploadFile


def calculate_sha256(file_obj: BinaryIO, chunk_size: int = 1024 * 1024) -> str:
    sha256 = hashlib.sha256()

    while chunk := file_obj.read(chunk_size):
        sha256.update(chunk)

    return sha256.hexdigest()


async def calculate_upload_file_checksum(upload_file: UploadFile) -> str:
    await upload_file.seek(0)
    checksum = calculate_sha256(upload_file.file)
    await upload_file.seek(0)

    return checksum
