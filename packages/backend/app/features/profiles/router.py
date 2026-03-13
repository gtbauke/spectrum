from uuid import UUID
from fastapi import APIRouter, Depends, status

from app.features.auth.guards.get_current_user import get_current_owner
from app.api.unit_of_work import get_uow

from core.ports.unit_of_work import UnitOfWork
from core.models.profiles.where import ProfilesWhere

from .service import ProfilesService, get_profiles_service
from .dto.create_profile import CreateProfileDTO, CreateProfileRouteDTO
from .dto.update_profile import UpdateProfileDTO, UpdateProfileRouteDTO

from .guards.is_profile_owner import is_profile_owner

profiles_router = APIRouter(
    tags=["profiles"],
)


@profiles_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(
    data: CreateProfileRouteDTO,
    uow: UnitOfWork = Depends(get_uow),
    profiles_service: ProfilesService = Depends(get_profiles_service),
    owner_id: UUID = Depends(get_current_owner),
):
    return await profiles_service.create(uow=uow, data=CreateProfileDTO(owner_id=owner_id, version=data.version))


@profiles_router.put(
    path="/{profile_id}",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(is_profile_owner)
    ]
)
async def update_profile(
    profile_id: UUID,
    data: UpdateProfileRouteDTO,
    uow: UnitOfWork = Depends(get_uow),
    profiles_service: ProfilesService = Depends(get_profiles_service),
    owner_id: UUID = Depends(get_current_owner),
):
    return await profiles_service.create_new_version(
        uow=uow,
        data=UpdateProfileDTO(owner_id=owner_id, version=data.version),
        where=ProfilesWhere(id=profile_id)
    )


@profiles_router.get(
    path="/{profile_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(is_profile_owner)
    ]
)
async def get_profile(
    profile_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    profiles_service: ProfilesService = Depends(get_profiles_service),
):
    return await profiles_service.get_unique(uow=uow, where=ProfilesWhere(id=profile_id))


@profiles_router.get(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def get_profiles(
    uow: UnitOfWork = Depends(get_uow),
    profiles_service: ProfilesService = Depends(get_profiles_service),
):
    return await profiles_service.get_all(uow=uow)
