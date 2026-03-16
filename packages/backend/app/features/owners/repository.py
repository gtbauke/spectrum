from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.core.repository import BaseRepositoryImplementation

from .models import OwnerORM

from core.repositories.owners import BaseOwnersRepository
from core.models.owners.owner import Owner
from core.models.owners.where import OwnersFilter, OwnerWhere


class OwnersRepository(BaseOwnersRepository, BaseRepositoryImplementation[
    Owner, OwnerORM, OwnerWhere, OwnersFilter
]):
    orm_model = OwnerORM

    async def get_unique(self, where: OwnerWhere) -> Owner | None:
        conditions = where.resolve(self.orm_model)

        query = (
            select(self.orm_model)
            .options(
                joinedload(self.orm_model.user),
            )
            .where(*conditions)
        )

        result = await self._session.execute(query)
        orm = result.scalar_one_or_none()

        return orm.to_domain() if orm else None
