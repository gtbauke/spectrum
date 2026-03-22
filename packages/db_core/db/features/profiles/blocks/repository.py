from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Iterable

from core.features.profiles.blocks.repository import IBlocksRepository
from core.features.profiles.blocks.block import Block
from core.features.profiles.blocks.where import BlockWhere, BlockFilter
from core.utils.pagination.base import Pagination
from core.utils.pagination.response import PaginatedResponse

from db.common.repositories.sql_alchemy_bulk_repository import SqlAlchemyBulkRepository

from .mapper import BlockMapper
from .model import BlockORM


class SqlAlchemyBlocksRepository(
    SqlAlchemyBulkRepository[BlockORM, Block,
                             BlockWhere, BlockFilter, BlockMapper],
    IBlocksRepository,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, BlockORM, BlockMapper)

    async def add(self, entity: Block) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._add(orm)

    async def update(self, entity: Block) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._update(orm)

    async def delete(self, entity: Block) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._delete(orm)

    async def add_many(self, entities: Iterable[Block]) -> None:
        orms = [self._mapper.to_orm(domain=entity) for entity in entities]
        await super()._add_many(orms)

    async def update_many(self, entities: Iterable[Block]) -> None:
        orms = [self._mapper.to_orm(domain=entity) for entity in entities]
        await super()._update_many(orms)

    async def delete_many(self, entities: Iterable[Block]) -> None:
        orms = [self._mapper.to_orm(domain=entity) for entity in entities]
        await super()._delete_many(orms)

    async def get_unique(self, where: BlockWhere) -> Block | None:
        return await super()._get_unique(where)

    async def list(self, filter: BlockFilter | None = None, pagination: Pagination | None = None) -> PaginatedResponse[Block]:
        resolved_filters = filter.resolve(
            self._model_class) if filter else None

        query = (
            select(self._model_class)
            .distinct()
        )

        if resolved_filters:
            query = query.where(*resolved_filters)

        if pagination:
            query = query.limit(pagination.limit).offset(pagination.offset)

        domains, total_count, current_page, total_pages, size = await self._paginate_query(
            query,
            pagination,
        )

        return PaginatedResponse(
            items=domains,
            total=total_count,
            pages=total_pages,
            page=current_page,
            size=size,
        )
