from core.common.repositories.base.immutable import IImmutableRepository
from core.common.repositories.base.mutable import IMutableRepository

from core.features.datasets.dataset import Dataset
from core.features.datasets.artifact import Artifact

from core.features.datasets.where import (
    DatasetWhere,
    DatasetFilter,
    ArtifactWhere,
    ArtifactFilter,
)


class IArtifactsRepository(IImmutableRepository[Artifact, ArtifactWhere, ArtifactFilter]):
    pass


class IDatasetsRepository(IMutableRepository[Dataset, DatasetWhere, DatasetFilter]):
    pass
