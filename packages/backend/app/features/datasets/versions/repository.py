from app.core.repository import BaseRepositoryImplementation

from ..models import DatasetVersionORM

from core.models.datasets.where import DatasetVersionsFilter, DatasetVersionsWhere
from core.models.datasets.dataset_version import DatasetVersion
from core.repositories.datasets import BaseDatasetVersionsRepository


class DatasetVersionsRepository(BaseDatasetVersionsRepository, BaseRepositoryImplementation[
    DatasetVersion,
    DatasetVersionORM,
    DatasetVersionsWhere,
    DatasetVersionsFilter
]):
    orm_model = DatasetVersionORM
