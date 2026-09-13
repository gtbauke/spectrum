from uuid import UUID
from datetime import datetime, timezone

from app.core.ports.unit_of_work import UnitOfWork
from app.core.utils.pagination.base import Pagination
from app.core.utils.pagination.response import PaginatedResponse
from app.features.profiles.domain.profile import Profile
from app.features.profiles.domain.where import ProfileWhere, ProfileFilter
from app.features.profiles.errors.profile_not_found import ProfileNotFound


class ProfilesService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def get_profile_by_id(self, profile_id: UUID) -> Profile:
        profile = await self._uow.profiles.get_unique(ProfileWhere(id=profile_id))
        if not profile:
            raise ProfileNotFound()
        return profile

    async def list_profiles(
        self,
        filter: ProfileFilter | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[Profile]:
        return await self._uow.profiles.list(filter=filter, pagination=pagination)

    async def delete_profile(self, profile_id: UUID) -> None:
        profile = await self.get_profile_by_id(profile_id)
        profile.deleted_at = datetime.now(tz=timezone.utc)
        await self._uow.profiles.update(profile)
