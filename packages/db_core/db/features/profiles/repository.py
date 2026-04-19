from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Sequence

from core.features.profiles.repository import IProfilesRepository
from core.features.profiles.profile import Profile
from core.features.profiles.where import ProfileWhere, ProfileFilter
from core.utils.pagination.base import Pagination
from core.utils.pagination.response import PaginatedResponse

from db.common.repositories.sql_alchemy_base_repository import SqlAlchemyBaseRepository
from db.features.profiles.blocks.inference.model import InferenceRunORM
from db.features.profiles.blocks.model import BlockORM

from .mapper import ProfilesMapper
from .model import ProfileORM


class SqlAlchemyProfilesRepository(
    SqlAlchemyBaseRepository[ProfileORM, Profile,
                             ProfileWhere, ProfileFilter, ProfilesMapper],
    IProfilesRepository,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ProfileORM, ProfilesMapper)

    async def add(self, entity: Profile) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._add(entity=orm)

    async def update(self, entity: Profile) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._update(entity=orm)

    async def delete(self, entity: Profile) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._delete(entity=orm)

    async def get_unique(self, where: ProfileWhere) -> Profile | None:
        query = (
            select(self._model_class)
            .options(
                selectinload(self._model_class.datasets),
                selectinload(self._model_class.blocks)
                .selectinload(BlockORM.inference_runs)
                .selectinload(InferenceRunORM.results),
                selectinload(self._model_class.jobs),
                selectinload(self._model_class.models),
            )
            .where(*where.resolve(self._model_class))
        )

        result = await self._session.execute(statement=query)
        orm = result.scalar_one_or_none()

        if not orm:
            return None

        return self._mapper.to_domain(orm=orm)

    def _build_query(
        self,
        filter: ProfileFilter | None = None,
    ):
        resolved_filters = filter.resolve(
            self._model_class) if filter else None

        query = (
            select(self._model_class)
            .options(
                selectinload(self._model_class.datasets),
                selectinload(self._model_class.blocks)
                .selectinload(BlockORM.inference_runs)
                .selectinload(InferenceRunORM.results),
                selectinload(self._model_class.jobs),
                selectinload(self._model_class.models),
            )
            .distinct()
        )

        if resolved_filters:
            query = query.where(*resolved_filters)

        return query

    async def list(
        self,
        filter: ProfileFilter | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[Profile]:
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
            pages=total_pages,
            page=current_page,
            size=size,
        )

    async def list_all(
        self,
        filter: ProfileFilter | None = None,
    ) -> Sequence[Profile]:
        query = self._build_query(filter=filter)
        return await self._list_all_query(query=query)

    async def list_recent(self, filter: ProfileFilter | None = None, max: int = 5) -> Sequence[Profile]:
        query = self._build_query(filter=filter)
        query = query.order_by(self._model_class.updated_at.desc()).limit(max)

        return await self._list_all_query(query=query)
