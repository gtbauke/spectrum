import logging
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status, Query, UploadFile, File

from app.api.response import PaginatedResponse
from app.api.unit_of_work import get_uow
from app.features.auth.guards.get_current_user import get_optional_current_owner, get_current_owner
from app.features.jobs.router import jobs_router

from app.features.profiles.errors.profile_not_found import ProfileNotFound
from app.features.profiles.responses.profile_details import ProfileDetails
from app.features.profiles.responses.profile_summary import ProfileSummary
from app.features.profiles.utils.profile_filter_builder import ProfileFilterBuilder
from app.features.users.responses.user_details import UserDetails
from app.features.owners.responses.owner_details import OwnerDetails
from app.features.owners.loaders.get_current_owner import (
    get_current_owner as get_owner_entity,
)

from core.models.owners.owner import Owner
from core.models.profiles.profile_dataset_role import ProfileDatasetRole
from core.models.profiles.profile_status import ProfileStatus
from core.models.profiles.profile_visibility import ProfileVisibility
from core.ports.unit_of_work import UnitOfWork
from core.models.profiles.where import ProfileDatasetAssociationFilter, ProfileVersionFilter, ProfileFilter, ProfileWhere
from core.utils.filters.field_filter import EnumFilter, NumberFilter, StringFilter, UUIDFilter

from .service import ProfilesService, get_profiles_service
from .dto.create_profile import CreateProfileDTO, CreateProfileFromDataset, CreateProfileFromDatasetRoute, CreateProfileRouteDTO
from .dto.update_profile import UpdateProfileDTO, UpdateProfileRouteDTO
from .associations.dto.create_association import CreateAssociationDTO, CreateAssociationRouteDTO
from .blocks.dto.create_block import CreateBlocks

from .guards.is_profile_owner import is_profile_owner

logger = logging.getLogger(__name__)
profiles_router = APIRouter(
    tags=["profiles"],
)

profiles_router.include_router(
    prefix="/{profile_id}/jobs",
    router=jobs_router,
)


@profiles_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(
    data: CreateProfileRouteDTO,
    uow: UnitOfWork = Depends(get_uow),
    profiles_service: ProfilesService = Depends(get_profiles_service),
    owner: Owner = Depends(get_owner_entity),
):
    return await profiles_service.create(
        uow=uow,
        data=CreateProfileDTO(
            owner=owner,
            version=data.version
        )
    )


@profiles_router.get(
    path="/summary",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[ProfileSummary],
)
async def get_profiles_summary(
    uow: UnitOfWork = Depends(get_uow),
    size: int = Query(20, ge=1, le=100),
    page: int = Query(1, ge=1),
    builder: ProfileFilterBuilder = Depends(),
):
    filter = builder.build()

    offset = (page - 1) * size
    result = await uow.profiles.get_profiles_summary(
        filter=filter,
        limit=size,
        offset=offset,
    )

    summaries = [
        ProfileSummary.from_profile(profile)
        for profile in result.items
    ]

    return PaginatedResponse(
        items=summaries,
        page=page,
        pages=(result.total + size - 1) // size,
        size=size,
        total=result.total,
    )


@profiles_router.post(
    path="/from-dataset",
    status_code=status.HTTP_201_CREATED,
)
async def create_profile_from_dataset(
    owner: Owner = Depends(get_owner_entity),
    data: CreateProfileFromDatasetRoute = Depends(
        CreateProfileFromDatasetRoute.as_form),
    file: UploadFile = File(...),
    uow: UnitOfWork = Depends(get_uow),
    profiles_service: ProfilesService = Depends(get_profiles_service),
):
    return await profiles_service.create_new_profile_from_dataset(
        uow=uow,
        data=CreateProfileFromDataset(
            owner=owner,
            file=file.file,
            dataset_name=data.dataset_name,
            dataset_description=data.dataset_description,
            dataset_role=data.dataset_role,
        )
    )


@profiles_router.get(
    path="/{profile_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProfileDetails,
)
async def get_profile_with_latest_version(
    profile_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
):
    profile_with_latest = await uow.profiles.get_with_latest_version(
        where=ProfileWhere(
            id=profile_id,
        )
    )

    if not profile_with_latest:
        raise ProfileNotFound()

    return ProfileDetails.from_profile(profile_with_latest)


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
        where=ProfileWhere(id=profile_id)
    )


@profiles_router.get(
    path="",
    status_code=status.HTTP_200_OK,
)
async def get_profiles(
    uow: UnitOfWork = Depends(get_uow),
    profiles_service: ProfilesService = Depends(get_profiles_service),
    owner_id: Optional[UUID] = Depends(get_optional_current_owner),
    size: int = Query(20, ge=1, le=100),
    page: int = Query(1, ge=1),
    version: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    status: ProfileStatus = Query(ProfileStatus.ACTIVE),
    visibility: ProfileVisibility = Query(ProfileVisibility.PUBLIC),
    role: Optional[ProfileDatasetRole] = Query(None),
    only_me: bool = Query(False),
):
    has_profile_version_dataset_filter = any([
        role is not None,
    ])

    has_profile_version_filter = any([
        version is not None,
        name is not None,
        description is not None,
        status is not None,
        visibility is not None,
        has_profile_version_dataset_filter,
    ])

    versions_filter = ProfileVersionFilter(
        version=NumberFilter[int](eq=version),
        name=StringFilter(ilike=f"%{name}%") if name else None,
        description=StringFilter(
            ilike=f"%{description}%") if description else None,
        status=EnumFilter[ProfileStatus](eq=status),
        visibility=EnumFilter[ProfileVisibility](eq=visibility),
        datasets=ProfileDatasetAssociationFilter(
            role=EnumFilter[ProfileDatasetRole](eq=role) if role else None,
        ) if has_profile_version_dataset_filter else None,
    ) if has_profile_version_filter else None

    filter = ProfileFilter(
        OR=[
            ProfileFilter(
                owner_id=UUIDFilter(eq=owner_id) if only_me else None,
                versions=versions_filter,
            ),
            ProfileFilter(
                owner_id=UUIDFilter(eq=owner_id) if only_me else None,
                versions=versions_filter.model_copy(
                    update={
                        "visibility": None,
                    }
                ) if versions_filter is not None else None,
            )
        ]
    )

    offset = (page - 1) * size
    items, total = await profiles_service.get_paginated(uow=uow, filter=filter, limit=size, offset=offset)

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@profiles_router.post(
    path="/{profile_id}/{profile_version_id}/datasets",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(is_profile_owner)
    ]
)
async def associate_dataset(
    profile_version_id: UUID,
    data: CreateAssociationRouteDTO,
    uow: UnitOfWork = Depends(get_uow),
    profiles_service: ProfilesService = Depends(get_profiles_service),
):
    return await profiles_service.associate_dataset(
        uow=uow,
        data=CreateAssociationDTO(
            profile_version_id=profile_version_id,
            dataset_version_id=data.dataset_version_id,
            role=data.role
        )
    )


@profiles_router.post(
    "/{profile_id}/blocks",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(is_profile_owner)
    ]
)
async def create_blocks(
    profile_id: UUID,
    blocks: CreateBlocks,
    uow: UnitOfWork = Depends(get_uow),
    profiles_service: ProfilesService = Depends(get_profiles_service),
    owner_id: UUID = Depends(get_current_owner),
):
    where = ProfileWhere(id=profile_id)
    return await profiles_service.create_new_version_from_blocks(
        uow=uow,
        blocks=blocks,
        where=where,
    )
