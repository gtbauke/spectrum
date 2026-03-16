from sqlalchemy import update

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

    async def unset_latest_version(self, *, where: DatasetVersionsWhere):
        await self._session.execute(
            update(self.orm_model)
            .where(
                *where.resolve(self.orm_model),
                self.orm_model.is_latest == True
            )
            .values(is_latest=False)
        )
