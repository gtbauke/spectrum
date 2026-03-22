from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from core.features.datasets.repository import IDatasetsRepository, IArtifactsRepository
from core.features.datasets.dataset import Dataset
from core.features.datasets.artifact import Artifact
from core.features.datasets.where import DatasetWhere, DatasetFilter, ArtifactWhere, ArtifactFilter
from core.utils.pagination.base import Pagination
from core.utils.pagination.response import PaginatedResponse

from db.common.repositories.sql_alchemy_base_repository import SqlAlchemyBaseRepository

from .mapper import DatasetsMapper, ArtifactMapper
from .model import DatasetORM, ArtifactORM


class SqlAlchemyDatasetsRepository(
    SqlAlchemyBaseRepository[DatasetORM, Dataset,
                             DatasetWhere, DatasetFilter, DatasetsMapper],
    IDatasetsRepository,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, DatasetORM, DatasetsMapper)

    async def add(self, entity: Dataset) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._add(entity=orm)

    async def update(self, entity: Dataset) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._update(entity=orm)

    async def delete(self, entity: Dataset) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._delete(entity=orm)

    async def get_unique(self, where: DatasetWhere) -> Dataset | None:
        return await super()._get_unique(where=where)

    def _build_query(
        self,
        filter: DatasetFilter | None = None,
    ):
        resolved_filters = filter.resolve(
            self._model_class) if filter else None

        query = (
            select(self._model_class)
            .options(
                selectinload(self._model_class.artifacts),
            )
            .distinct()
        )

        if resolved_filters:
            query = query.where(*resolved_filters)
            
        return query

    async def list(
        self,
        filter: DatasetFilter | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[Dataset]:
        query = self._build_query(filter=filter)

        if pagination:
            query = query.limit(limit=pagination.limit).offset(offset=pagination.offset)

        domains, total_count, current_page, total_pages, size = await self._paginate_query(
            query=query,
            pagination=pagination,
        )

        return PaginatedResponse(
            items=domains,
            total=total_count,
            pages=total_pages,
            page=current_page,
            size=size,
        )

    async def list_all(
        self,
        filter: DatasetFilter | None = None,
    ) -> Sequence[Dataset]:
        query = self._build_query(filter=filter)
        return await self._list_all_query(query=query)


class SqlAlchemyArtifactsRepository(
    SqlAlchemyBaseRepository[ArtifactORM, Artifact,
                             ArtifactWhere, ArtifactFilter, ArtifactMapper],
    IArtifactsRepository,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ArtifactORM, ArtifactMapper)

    async def add(self, entity: Artifact) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._add(entity=orm)

    async def get_unique(self, where: ArtifactWhere) -> Artifact | None:
        return await super()._get_unique(where=where)

    def _build_query(
        self,
        filter: ArtifactFilter | None = None,
    ):
        resolved_filters = filter.resolve(
            self._model_class) if filter else None

        query = select(self._model_class).distinct()

        if resolved_filters:
            query = query.where(*resolved_filters)
            
        return query

    async def list(
        self,
        filter: ArtifactFilter | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[Artifact]:
        query = self._build_query(filter=filter)

        if pagination:
            query = query.limit(limit=pagination.limit).offset(offset=pagination.offset)

        domains, total_count, current_page, total_pages, size = await self._paginate_query(
            query=query,
            pagination=pagination,
        )

        return PaginatedResponse(
            items=domains,
            total=total_count,
            pages=total_pages,
            page=current_page,
            size=size,
        )

    async def list_all(
        self,
        filter: ArtifactFilter | None = None,
    ) -> Sequence[Artifact]:
        query = self._build_query(filter=filter)
        return await self._list_all_query(query=query)
