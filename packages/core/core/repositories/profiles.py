from abc import abstractmethod
from uuid import UUID
from typing import Optional


from .base import BaseRepository, BaseVersionedRepository

from core.models.profiles.where import (
    ProfilesWhere,
    ProfilesFilter,
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


class BaseProfilesRepository(BaseRepository[Profile, ProfilesWhere, ProfilesFilter]):
    @abstractmethod
    async def get_owner_id(self, where: ProfilesWhere) -> Optional[UUID]:
        pass

    @abstractmethod
    async def get_paginated(self, *, filter: ProfilesFilter, limit: int = 20, offset: int = 0) -> tuple[list[Profile], int]:
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
