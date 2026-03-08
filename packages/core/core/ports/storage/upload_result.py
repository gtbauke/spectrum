from .path import SpectrumPath


class UploadResult:
    def __init__(self, path: SpectrumPath, size: int, checksum: str):
        self._path = path
        self._size = size
        self._checksum = checksum

    @property
    def path(self) -> SpectrumPath:
        return self._path

    @property
    def size(self) -> int:
        return self._size

    @property
    def checksum(self) -> str:
        return self._checksum
