from app.core.repository import BaseRepositoryImplementation

from .models import DatasetORM

from core.models.datasets.where import DatasetsFilter, DatasetsWhere
from core.models.datasets.dataset import Dataset
from core.repositories.datasets import BaseDatasetsRepository


class DatasetsRepository(BaseDatasetsRepository, BaseRepositoryImplementation[
    Dataset,
    DatasetORM,
    DatasetsWhere,
    DatasetsFilter
]):
    orm_model = DatasetORM
