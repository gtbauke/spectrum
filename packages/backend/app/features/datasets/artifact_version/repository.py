from app.core.repository import BaseRepositoryImplementation

from ..models import DatasetVersionArtifactAssociationORM

from core.models.datasets.where import DatasetArtifactVersionsFilter, DatasetArtifactVersionsWhere
from core.models.datasets.dataset_artifact_version import DatasetArtifactVersion
from core.repositories.datasets import BaseDatasetArtifactVersionsRepository


class DatasetArtifactVersionsRepository(BaseDatasetArtifactVersionsRepository, BaseRepositoryImplementation[
    DatasetArtifactVersion,
    DatasetVersionArtifactAssociationORM,
    DatasetArtifactVersionsWhere,
    DatasetArtifactVersionsFilter
]):
    orm_model = DatasetVersionArtifactAssociationORM
