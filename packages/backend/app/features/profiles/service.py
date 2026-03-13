import logging

from typing import Optional

from core.ports.unit_of_work import UnitOfWork

from core.services.base import BaseImmutableVersionedService
from core.models.profiles.profile import Profile
from core.models.profiles.profile_version import ProfileVersion
from core.models.profiles.where import ProfileVersionWhere, ProfilesWhere, ProfilesFilter
from core.utils.pagination.base import Pagination

from .dto.create_profile import CreateProfileDTO
from .dto.update_profile import UpdateProfileDTO

from .versions.errors.profile_version_not_found import ProfileVersionNotFound
from .errors.profile_not_found import ProfileNotFound

logger = logging.getLogger(__name__)


class ProfilesService(BaseImmutableVersionedService[
    Profile,
    ProfilesWhere,
    CreateProfileDTO,
    UpdateProfileDTO,
    ProfilesFilter
]):
    async def get_unique(self, *, uow: UnitOfWork, where: ProfilesWhere) -> Optional[Profile]:
        return await uow.profiles.get_unique(where=where)

    async def get_latest(self, *, uow: UnitOfWork, where: ProfilesWhere) -> Optional[Profile]:
        final_where = ProfilesWhere(id=where.id, is_latest=True)
        return await uow.profiles.get_unique(where=final_where)

    async def create(self, *, uow: UnitOfWork, data: CreateProfileDTO, version: int = 1) -> Profile:
        new_profile = Profile.new(owner_id=data.owner_id)

        if data.version:
            created_version = ProfileVersion.new(
                name=data.version.name,
                description=data.version.description,
                visibility=data.version.visibility,
                profile_id=new_profile.id,
                version=version,
                is_latest=True
            )

            new_profile.versions.append(created_version)

        profile = await uow.profiles.add(new_profile)
        return profile

    async def create_new_version(self, *, uow: UnitOfWork, data: UpdateProfileDTO, where: ProfilesWhere) -> Profile:
        latest_version = await uow.profile_versions.unset_latest(where=ProfileVersionWhere(profile_id=where.id, is_latest=True))

        if not latest_version:
            raise ProfileVersionNotFound()

        name_temp = latest_version.name if data.version is None else data.version.name
        name = name_temp if name_temp is not None else latest_version.name

        visibility_temp = latest_version.visibility if data.version is None else data.version.visibility
        visibility = visibility_temp if visibility_temp is not None else latest_version.visibility

        updated_latest_version = ProfileVersion.new(
            name=name,
            description=latest_version.description if data.version is None else data.version.description,
            visibility=visibility,
            profile_id=where.id,
            version=latest_version.version + 1,
            is_latest=True
        )

        await uow.profile_versions.add(updated_latest_version)
        profile = await uow.profiles.get_unique(where=where)

        if not profile:
            raise ProfileNotFound()

        return profile

    async def get_all(self, *, uow: UnitOfWork, filter: Optional[ProfilesFilter] = None,
                      pagination: Optional[Pagination] = None) -> list[Profile]:
        return await uow.profiles.list_all(where=filter, pagination=pagination)


def get_profiles_service() -> ProfilesService:
    return ProfilesService()
