from .immutable import IImmutableRepository
from .mutable import IMutableRepository
from .versioned import IVersionedRepository
from .bulk import IMutableBulkRepository

__all__ = [
    "IImmutableRepository",
    "IMutableRepository",
    "IVersionedRepository",
    "IMutableBulkRepository",
]
