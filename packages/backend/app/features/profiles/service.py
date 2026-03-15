import logging

from typing import Optional

from core.models.datasets.where import DatasetArtifactVersionsWhere
from core.models.profiles.profile_block import ProfileBlock
from core.models.profiles.profile_dataset_role import ProfileDatasetRole
from core.models.profiles.profile_visibility import ProfileVisibility
from core.ports.unit_of_work import UnitOfWork

from core.services.base import BaseImmutableVersionedService
from core.models.profiles.profile import Profile
from core.models.profiles.profile_version import ProfileVersion
from core.models.profiles.profile_dataset_association import ProfileDatasetAssociation
from core.models.profiles.where import ProfileVersionWhere, ProfilesWhere, ProfilesFilter
from core.utils.pagination.base import Pagination

from app.features.datasets.artifacts.dto.create_artifact import CreateArtifactDTO
from app.features.datasets.dto.create_dataset import CreateDatasetDTO
from app.features.datasets.artifacts.service import DatasetArtifactsService, get_dataset_artifacts_service
from app.features.datasets.service import DatasetsService, get_datasets_service

from .dto.create_profile import CreateProfileDTO, CreateProfileFromDataset
from .dto.update_profile import UpdateProfileDTO

from .versions.errors.profile_version_not_found import ProfileVersionNotFound
from .errors.profile_not_found import ProfileNotFound

from .associations.dto.create_association import CreateAssociationDTO
from .blocks.dto.create_block import CreateBlocks

logger = logging.getLogger(__name__)


class ProfilesService(BaseImmutableVersionedService[
    Profile,
    ProfilesWhere,
    CreateProfileDTO,
    UpdateProfileDTO,
    ProfilesFilter
]):
    def __init__(
        self,
        dataset_artifacts_service: DatasetArtifactsService,
        datasets_service: DatasetsService,
    ):
        self._dataset_artifacts_service = dataset_artifacts_service
        self._datasets_service = datasets_service

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

    async def associate_dataset(self, *, uow: UnitOfWork, data: CreateAssociationDTO) -> ProfileDatasetAssociation:
        association = ProfileDatasetAssociation.new(
            dataset_version_id=data.dataset_version_id,
            profile_version_id=data.profile_version_id,
            role=data.role
        )

        return await uow.profile_dataset_associations.add(association)

    async def get_paginated(self, *, uow: UnitOfWork, filter: ProfilesFilter, limit: int = 20, offset: int = 0) -> tuple[list[Profile], int]:
        return await uow.profiles.get_paginated(filter=filter, limit=limit, offset=offset)

    async def create_new_version_from_blocks(
        self,
        *,
        uow: UnitOfWork,
        blocks: CreateBlocks,
        where: ProfilesWhere,
    ):
        latest_version = await uow.profile_versions.unset_latest(where=ProfileVersionWhere(profile_id=where.id, is_latest=True))

        if not latest_version:
            raise ProfileVersionNotFound()

        new_blocks = [
            ProfileBlock.new(
                version_id=latest_version.id,
                order_index=block.order_index,
                type=block.type,
                data=block.get_json_data(),
            ) for block in blocks.blocks
        ]

        new_version_data = blocks.metadata_block.build_from_diff(
            latest_version)

        new_associations = [
            ProfileDatasetAssociation.new(
                dataset_version_id=association.dataset_version_id,
                profile_version_id=latest_version.id,
                role=association.role
            ) for association in latest_version.datasets
        ]

        new_version = ProfileVersion.new(
            name=new_version_data.name,
            description=new_version_data.description,
            visibility=new_version_data.visibility,
            profile_id=latest_version.profile_id,
            version=latest_version.version + 1,
            is_latest=True,
            blocks=new_blocks,
            datasets=new_associations,
        )

        await uow.profile_versions.add(new_version)
        profile = await uow.profiles.get_unique(where=where)

        if not profile:
            raise ProfileNotFound()

        return profile

    async def create_new_profile_from_dataset(
        self,
        *,
        uow: UnitOfWork,
        data: CreateProfileFromDataset
    ):
        dataset = await self._datasets_service.create(
            uow=uow,
            data=CreateDatasetDTO(
                owner_id=data.owner_id,
                name=data.dataset_name,
                description=data.dataset_description,
            )
        )

        latest_dataset_version = dataset.versions[0]
        await self._dataset_artifacts_service.create(
            uow=uow,
            data=CreateArtifactDTO(
                dataset_id=dataset.id,
                dataset_version_id=latest_dataset_version.id,
            ),
            file=data.file,
        )

        profile = await uow.profiles.add(Profile.new(
            owner_id=data.owner_id,
        ))

        profile_version = await uow.profile_versions.add(ProfileVersion.new(
            name=f"Profile for {data.dataset_name}",
            description=f"Profile for {data.dataset_name}",
            version=1,
            is_latest=True,
            profile_id=profile.id,
            visibility=ProfileVisibility.PRIVATE,
            blocks=[],
            datasets=[],
        ))

        dataset_associations = ProfileDatasetAssociation.new(
            dataset_version_id=latest_dataset_version.id,
            profile_version_id=profile_version.id,
            role=data.dataset_role,
        )

        await uow.profile_dataset_associations.add(dataset_associations)

        final_profile = await uow.profiles.get_unique(
            where=ProfilesWhere(id=profile.id)
        )

        return final_profile


def get_profiles_service() -> ProfilesService:
    dataset_artifacts = get_dataset_artifacts_service()
    datasets = get_datasets_service()

    return ProfilesService(
        dataset_artifacts_service=dataset_artifacts,
        datasets_service=datasets,
    )
