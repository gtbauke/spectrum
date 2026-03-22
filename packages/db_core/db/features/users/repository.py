from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from core.features.users.repository import IUsersRepository
from core.features.users.user import User
from core.features.users.where import UserWhere, UserFilter
from core.utils.pagination.base import Pagination
from core.utils.pagination.response import PaginatedResponse

from db.common.repositories.sql_alchemy_base_repository import SqlAlchemyBaseRepository

from .mapper import UsersMapper
from .model import UserORM


class SqlAlchemyUsersRepository(
    SqlAlchemyBaseRepository[UserORM, User,
                             UserWhere, UserFilter, UsersMapper],
    IUsersRepository,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserORM, UsersMapper)

    async def add(self, entity: User) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._add(entity=orm)

    async def update(self, entity: User) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._update(entity=orm)

    async def delete(self, entity: User) -> None:
        orm = self._mapper.to_orm(domain=entity)
        await super()._delete(entity=orm)

    async def get_unique(self, where: UserWhere) -> User | None:
        query = (
            select(self._model_class)
            .where(*where.resolve(self._model_class))
        )

        result = await self._session.execute(statement=query)
        orm = result.scalar_one_or_none()

        if not orm:
            return None

        return self._mapper.to_domain(orm=orm)

    def _build_query(
        self,
        filter: UserFilter | None = None,
    ):
        resolved_filters = filter.resolve(
            self._model_class) if filter else None

        query = select(self._model_class).distinct()

        if resolved_filters:
            query = query.where(*resolved_filters)

        return query

    async def list(
        self,
        filter: UserFilter | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[User]:
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
        filter: UserFilter | None = None,
    ) -> Sequence[User]:
        query = self._build_query(filter=filter)
        return await self._list_all_query(query=query)
