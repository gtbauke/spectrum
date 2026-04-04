import logging
from uuid import UUID
from fastapi import APIRouter, Depends, status, UploadFile, File, Form, Query

from app.api.unit_of_work import get_uow
from app.features.datasets.errors.dataset_not_found import DatasetNotFound
from app.features.profiles.dtos.link import LinkDatasetToProfile
from app.features.profiles.responses.profile_summary import ProfileSummary
from core.features.datasets.where import DatasetWhere
from core.features.profiles.blocks.block import Block
from core.features.profiles.blocks.where import BlockWhere
from core.ports.unit_of_work import UnitOfWork

from app.features.auth.guards.get_current_user import get_current_user
from app.features.profiles.errors.profile_not_found import ProfileNotFound
from app.features.profiles.dtos.create import CreateProfileDto
from app.features.profiles.dtos.update import UpdateProfileDto
from app.features.profiles.guards.can_edit_profile import can_edit_profile

from core.features.profiles.profile import Profile
from core.features.profiles.profile_mode import ProfileMode
from core.features.profiles.where import ProfileWhere, ProfileFilter

from core.features.datasets.dataset import Dataset
from core.features.datasets.artifact import Artifact
from core.features.datasets.artifact_role import ArtifactRole

from core.utils.pagination.base import Pagination
from core.utils.filters.field_filter import UUIDFilter, StringFilter, EnumFilter

from app.features.profiles.blocks.routers.blocks import blocks_router
from app.features.profiles.jobs.routers.jobs import jobs_router
from app.features.profiles.models.routers.models import models_router
from db.features.auth.repository import PaginatedResponse

profiles_router = APIRouter()

profiles_router.include_router(
    blocks_router, prefix="/{profile_id}/blocks", tags=["Blocks"])

profiles_router.include_router(
    jobs_router, prefix="/{profile_id}/jobs", tags=["Jobs"])

profiles_router.include_router(
    models_router, prefix="/{profile_id}/models", tags=["Models"])

logger = logging.getLogger(__name__)


@profiles_router.post(
    path="",
    response_model=Profile,
    status_code=status.HTTP_201_CREATED
)
async def create_profile(
    dto: CreateProfileDto,
    current_user_id: UUID = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    profile = Profile.new(
        name=dto.name,
        description=dto.description,
        owner_id=current_user_id,
        mode=ProfileMode.DRAFT
    )

    await uow.profiles.add(profile)
    return profile


@profiles_router.post(
    path="/{profile_id}/datasets",
    response_model=Profile,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(can_edit_profile)]
)
async def link_dataset_to_profile(
    dto: LinkDatasetToProfile,
    profile_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    profile = await uow.profiles.get_unique(ProfileWhere(id=profile_id))

    if not profile:
        raise ProfileNotFound()

    for dataset_id in dto.dataset_ids:
        dataset = await uow.datasets.get_unique(DatasetWhere(id=dataset_id))

        if not dataset:
            raise DatasetNotFound()

        profile.datasets.append(dataset)

    await uow.profiles.update(profile)
    return profile


@profiles_router.post(
    path="/from-dataset",
    response_model=Profile,
    status_code=status.HTTP_201_CREATED
)
async def create_profile_from_dataset(
    profile_name: str = Form(...),
    profile_description: str = Form(""),
    dataset_name: str = Form(...),
    dataset_description: str = Form(""),
    file: UploadFile = File(...),
    current_user_id: UUID = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    profile = Profile.new(
        name=profile_name,
        description=profile_description,
        owner_id=current_user_id,
        mode=ProfileMode.DRAFT
    )

    dataset = Dataset.new(
        name=dataset_name,
        description=dataset_description,
        owner_id=current_user_id
    )

    profile.datasets.append(dataset)

    path = f"datasets/{dataset.id}/artifacts/{file.filename}"
    upload_result = await uow.file_storage.upload(path=path, file=file.file)

    artifact = Artifact(
        dataset_id=dataset.id,
        checksum=upload_result.checksum,
        size_in_bytes=upload_result.size,
        path=upload_result.path,
        role=ArtifactRole.DATA
    )

    dataset.artifacts.append(artifact)
    await uow.profiles.add(profile)

    return profile


@profiles_router.get("", response_model=PaginatedResponse[Profile])
async def list_profiles(
    limit: int = Query(50, ge=1),
    offset: int = Query(0, ge=0),
    mine: bool = Query(
        False, description="Filter profiles owned by the current user"),
    name: str | None = Query(None, description="Filter profiles by name"),
    description: str | None = Query(
        None, description="Filter profiles by description"),
    mode: ProfileMode | None = Query(
        None, description="Filter profiles by mode"),
    current_user_id: UUID = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
):
    pagination = Pagination(limit=limit, offset=offset)
    profile_filter = ProfileFilter()

    if mine:
        profile_filter.owner_id = UUIDFilter(eq=current_user_id)

    if name:
        profile_filter.name = StringFilter(eq=name)

    if description:
        profile_filter.description = StringFilter(eq=description)

    if mode:
        profile_filter.mode = EnumFilter(eq=mode)

    paginated_response = await uow.profiles.list(filter=profile_filter, pagination=pagination)
    return paginated_response


@profiles_router.get(
    path="/summary",
    response_model=list[ProfileSummary],
)
async def get_profiles_summary(
    uow: UnitOfWork = Depends(get_uow)
):
    profiles = await uow.profiles.list_all()
    summaries = [ProfileSummary.from_profile(profile) for profile in profiles]

    return summaries


@profiles_router.get(
    path="/{profile_id}",
    response_model=Profile,
    dependencies=[Depends(get_current_user)]
)
async def get_profile(
    profile_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    profile = await uow.profiles.get_unique(ProfileWhere(id=profile_id))
    if not profile:
        raise ProfileNotFound()
    return profile


@profiles_router.put(
    path="/{profile_id}",
    response_model=Profile,
    dependencies=[Depends(can_edit_profile)]
)
async def update_profile(
    profile_id: UUID,
    dto: UpdateProfileDto,
    uow: UnitOfWork = Depends(get_uow)
):
    logger.info(f"Updating profile {profile_id}", extra={
        "dto": dto.model_dump(exclude_unset=True),
        "profile_id": profile_id
    })

    profile = await uow.profiles.get_unique(ProfileWhere(id=profile_id))

    if not profile:
        raise ProfileNotFound()

    updated_profile = profile.model_copy(
        update=dto.model_dump(exclude_unset=True, exclude={"blocks"})
    )

    await uow.profiles.update(updated_profile)

    if dto.blocks is not None:
        blocks_to_create: list[Block] = []
        blocks_to_update: list[Block] = []

        for block in dto.blocks:
            block_exists = await uow.blocks.get_unique(where=BlockWhere(id=block.id))

            if not block_exists:
                blocks_to_create.append(block)
            else:
                blocks_to_update.append(block)

        await uow.blocks.add_many(blocks_to_create)
        await uow.blocks.update_many(blocks_to_update)

    return updated_profile


@profiles_router.delete(
    path="/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(can_edit_profile)]
)
async def delete_profile(
    profile_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    profile = await uow.profiles.get_unique(ProfileWhere(id=profile_id))

    if not profile:
        raise ProfileNotFound()

    await uow.profiles.delete(profile)
    return None
