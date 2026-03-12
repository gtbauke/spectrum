import logging

from typing import Optional

from core.ports.unit_of_work import UnitOfWork

from core.services.base import BaseCRUDService
from core.models.profiles.profile import Profile
from core.models.profiles.profile_version import ProfileVersion
from core.models.profiles.where import ProfilesWhere, ProfilesFilter

from .dto.create_profile import CreateProfileDTO
from .dto.update_profile import UpdateProfileDTO
from .errors.profile_not_found import ProfileNotFound

logger = logging.getLogger(__name__)


class ProfilesService(BaseCRUDService[
    Profile,
    ProfilesWhere,
    CreateProfileDTO,
    UpdateProfileDTO,
    ProfilesFilter
]):
    async def get_unique(self, *, uow: UnitOfWork, where: ProfilesWhere) -> Optional[Profile]:
        return await uow.profiles.get_unique(where=where)

    async def create(self, *, uow: UnitOfWork, data: CreateProfileDTO) -> Profile:
        logger.info("Creating profile", extra={
            "data": data.model_dump(),
        })

        new_profile = Profile.new(owner_id=data.owner_id)

        if data.version:
            initial_version = ProfileVersion.new(
                name=data.version.name,
                description=data.version.description,
                visibility=data.version.visibility,
                profile_id=new_profile.id,
                version=1,
                is_latest=True
            )

            new_profile.versions.append(initial_version)

        profile = await uow.profiles.add(new_profile)
        return profile

    async def update_unique(self, *, uow: UnitOfWork, where: ProfilesWhere, data: UpdateProfileDTO) -> Profile:
        profile = await uow.profiles.get_unique(where=where)

        if not profile:
            raise ProfileNotFound()

        update_data = data.model_dump(exclude_unset=True)
        updated_profile = profile.model_copy(
            update=update_data)

        return await uow.profiles.update(updated_profile)

    async def delete_unique(self, *, uow: UnitOfWork, where: ProfilesWhere):
        return await uow.profiles.delete(where=where)

    async def get_all(self, *, uow: UnitOfWork, filter: Optional[ProfilesFilter] = None) -> list[Profile]:
        return await uow.profiles.list_all(where=filter)


def get_profiles_service() -> ProfilesService:
    return ProfilesService()
