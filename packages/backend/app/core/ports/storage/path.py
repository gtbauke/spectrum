from pathlib import Path


class SpectrumPath:
    def __init__(self, full_path: Path, path: Path):
        self._full_path = full_path
        self._path = path

    @property
    def full_path(self) -> Path:
        return self._full_path

    @property
    def path(self) -> Path:
        return self._path
