from abc import abstractmethod
from uuid import UUID
from typing import Optional

from app.api.response import RepositoryPaginatedResponse
from .base import BaseRepository, BaseVersionedRepository

from core.models.profiles.where import (
    ProfileWhere,
    ProfileFilter,
    ProfileVersionWhere,
    ProfileVersionFilter,
    ProfileDatasetAssociationWhere,
    ProfileDatasetAssociationFilter,
    ProfileBlockWhere,
    ProfileBlockFilter
)
from core.models.profiles.profile import Profile
from core.models.profiles.profile_version import ProfileVersion
from core.models.profiles.profile_block import ProfileBlock
from core.models.profiles.profile_dataset_association import ProfileDatasetAssociation


class BaseProfilesRepository(BaseRepository[Profile, ProfileWhere, ProfileFilter]):
    @abstractmethod
    async def get_owner_id(self, where: ProfileWhere) -> Optional[UUID]:
        pass

    @abstractmethod
    async def get_paginated(self, *, filter: ProfileFilter, limit: int = 20, offset: int = 0) -> tuple[list[Profile], int]:
        ...

    @abstractmethod
    async def get_profiles_summary(self, *, filter: ProfileFilter, limit: int, offset: int) -> RepositoryPaginatedResponse[Profile]:
        ...

    @abstractmethod
    async def get_with_latest_version(self, *, where: ProfileWhere) -> Optional[Profile]:
        ...


class BaseProfileVersionsRepository(BaseVersionedRepository[
    ProfileVersion,
    ProfileVersionWhere,
    ProfileVersionFilter
]):
    pass


class BaseProfileDatasetAssociationsRepository(BaseRepository[
    ProfileDatasetAssociation,
    ProfileDatasetAssociationWhere,
    ProfileDatasetAssociationFilter
]):
    pass


class BaseProfileBlocksRepository(BaseRepository[
    ProfileBlock,
    ProfileBlockWhere,
    ProfileBlockFilter
]):
    pass
