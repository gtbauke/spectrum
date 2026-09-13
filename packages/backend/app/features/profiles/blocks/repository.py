from typing import Protocol, Iterable, Sequence
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.ports.repositories.bulk import IMutableBulkRepository
from app.core.utils.pagination.base import Pagination
from app.core.utils.pagination.response import PaginatedResponse
from app.core.database.repositories.sql_alchemy_bulk_repository import SqlAlchemyBulkRepository

from app.features.profiles.blocks.domain.block import Block
from app.features.profiles.blocks.domain.where import BlockWhere, BlockFilter
from app.features.profiles.blocks.inference.model import InferenceRunORM
from .mapper import BlockMapper
from .model import BlockORM


class IBlocksRepository(IMutableBulkRepository[Block, BlockWhere, BlockFilter], Protocol):
    pass


class SqlAlchemyBlocksRepository(
    SqlAlchemyBulkRepository[BlockORM, Block,
                             BlockWhere, BlockFilter, BlockMapper],
    IBlocksRepository,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, BlockORM, BlockMapper)

    async def add(self, entity: Block) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._add(entity=orm)

    async def update(self, entity: Block) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._update(entity=orm)

    async def delete(self, entity: Block) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._delete(entity=orm)

    async def add_many(self, entities: Iterable[Block]) -> None:
        orms = [self._mapper.to_orm(domain=entity) for entity in entities]
        await super()._add_many(entities=orms)

    async def update_many(self, entities: Iterable[Block]) -> None:
        orms = [self._mapper.to_orm(domain=entity) for entity in entities]
        await super()._update_many(entities=orms)

    async def delete_many(self, entities: Iterable[Block]) -> None:
        orms = [self._mapper.to_orm(domain=entity) for entity in entities]
        await super()._delete_many(entities=orms)

    async def get_unique(self, where: BlockWhere) -> Block | None:
        return await super()._get_unique(
            where,
            selectinload(BlockORM.inference_runs).selectinload(
                InferenceRunORM.results)
        )

    def _build_query(
        self,
        filter: BlockFilter | None = None,
    ):
        resolved_filters = filter.resolve(
            self._model_class) if filter else None

        query = select(self._model_class).options(
            selectinload(self._model_class.inference_runs).selectinload(
                InferenceRunORM.results)
        ).distinct()

        if resolved_filters:
            query = query.where(*resolved_filters)

        return query

    async def list(
        self,
        filter: BlockFilter | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[Block]:
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
        filter: BlockFilter | None = None,
    ) -> Sequence[Block]:
        query = self._build_query(filter=filter)
        return await self._list_all_query(query=query)
