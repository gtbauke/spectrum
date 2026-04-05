from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Iterable

from core.features.profiles.blocks.inference.repository import IInferenceRunRepository, IInferenceResultRepository
from core.features.profiles.blocks.inference.inference_run import InferenceRun
from core.features.profiles.blocks.inference.inference_result import InferenceResult
from core.features.profiles.blocks.inference.where import (
    InferenceRunWhere, InferenceRunFilter,
    InferenceResultWhere, InferenceResultFilter
)
from core.utils.pagination.base import Pagination
from core.utils.pagination.response import PaginatedResponse
from db.common.repositories.sql_alchemy_base_repository import SqlAlchemyBaseRepository
from .mapper import InferenceRunMapper, InferenceResultMapper
from .model import InferenceRunORM, InferenceResultORM


class SqlAlchemyInferenceRunRepository(
    SqlAlchemyBaseRepository[InferenceRunORM, InferenceRun,
                             InferenceRunWhere, InferenceRunFilter, InferenceRunMapper],
    IInferenceRunRepository
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, InferenceRunORM, InferenceRunMapper)

    async def get_unique(self, where: InferenceRunWhere) -> InferenceRun | None:
        return await super()._get_unique(where)

    async def add(self, entity: InferenceRun) -> None:
        return await super()._add(self._mapper.to_orm(entity))

    async def get_latest_version(self, parent_id: UUID) -> InferenceRun | None:
        # parent_id is block_id for this repo
        query = select(self._model_class).where(
            self._model_class.block_id == parent_id,
            self._model_class.is_latest == True
        )
        result = await self._session.execute(query)
        orm = result.scalars().first()
        return self._mapper.to_domain(orm) if orm else None

    async def get_version_by_number(self, parent_id: UUID, version: int) -> InferenceRun | None:
        query = select(self._model_class).where(
            self._model_class.block_id == parent_id,
            self._model_class.version == version
        )
        result = await self._session.execute(query)
        orm = result.scalars().first()
        return self._mapper.to_domain(orm) if orm else None

    async def unset_latest_and_add(self, parent_id: UUID, new_entity: InferenceRun) -> None:
        # parent_id is block_id
        await self._session.execute(
            update(self._model_class)
            .where(self._model_class.block_id == parent_id, self._model_class.is_latest == True)
            .values(is_latest=False)
        )

        orm = self._mapper.to_orm(new_entity)
        await self._add(orm)

    def _build_query(
        self,
        filter: InferenceRunFilter | None = None,
    ):
        resolved_filters = filter.resolve(
            self._model_class) if filter else None

        query = select(self._model_class).distinct()

        if resolved_filters:
            query = query.where(*resolved_filters)

        return query

    async def list(
        self,
        filter: InferenceRunFilter | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[InferenceRun]:
        query = self._build_query(filter=filter)

        if pagination:
            query = query.limit(limit=pagination.limit).offset(
                offset=pagination.offset)

        domains, total_count, current_page, total_pages, size = await self._paginate_query(
            query=query,
            pagination=pagination,
        )

        return PaginatedResponse(
            items=domains,
            total=total_count,
            page=current_page,
            pages=total_pages,
            size=size,
        )

    async def list_all(
        self,
        filter: InferenceRunFilter | None = None,
    ) -> Sequence[InferenceRun]:
        query = self._build_query(filter=filter)
        return await self._list_all_query(query=query)


class SqlAlchemyInferenceResultRepository(
    SqlAlchemyBaseRepository[InferenceResultORM, InferenceResult,
                             InferenceResultWhere, InferenceResultFilter, InferenceResultMapper],
    IInferenceResultRepository
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, InferenceResultORM, InferenceResultMapper)

    async def add_many(self, entities: Iterable[InferenceResult]) -> None:
        orms = [self._mapper.to_orm(e) for e in entities]
        self._session.add_all(orms)

    async def get_unique(self, where: InferenceResultWhere) -> InferenceResult | None:
        return await super()._get_unique(where)

    async def add(self, entity: InferenceResult) -> None:
        return await super()._add(self._mapper.to_orm(entity))

    def _build_query(
        self,
        filter: InferenceResultFilter | None = None,
    ):
        resolved_filters = filter.resolve(
            self._model_class) if filter else None

        query = select(self._model_class).distinct()

        if resolved_filters:
            query = query.where(*resolved_filters)

        return query

    async def list(
        self,
        filter: InferenceResultFilter | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[InferenceResult]:
        query = self._build_query(filter=filter)

        if pagination:
            query = query.limit(limit=pagination.limit).offset(
                offset=pagination.offset)

        domains, total_count, current_page, total_pages, size = await self._paginate_query(
            query=query,
            pagination=pagination,
        )

        return PaginatedResponse(
            items=domains,
            total=total_count,
            page=current_page,
            pages=total_pages,
            size=size,
        )

    async def list_all(
        self,
        filter: InferenceResultFilter | None = None,
    ) -> Sequence[InferenceResult]:
        query = self._build_query(filter=filter)
        return await self._list_all_query(query=query)
