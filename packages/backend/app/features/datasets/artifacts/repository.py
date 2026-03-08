from app.core.repository import BaseRepositoryImplementation

from ..models import DatasetArtifactORM

from core.models.datasets.where import DatasetArtifactsFilter, DatasetArtifactsWhere
from core.models.datasets.dataset_artifact import DatasetArtifact
from core.repositories.datasets import BaseDatasetArtifactsRepository


class DatasetArtifactsRepository(BaseDatasetArtifactsRepository, BaseRepositoryImplementation[
    DatasetArtifact,
    DatasetArtifactORM,
    DatasetArtifactsWhere,
    DatasetArtifactsFilter
]):
    orm_model = DatasetArtifactORM
