from .base import BaseRepository

from core.models.profiles.where import (
    ProfilesWhere,
    ProfilesFilter,
    ProfileVersionWhere,
    ProfileVersionFilter,
    ProfileDatasetAssociationWhere,
    ProfileDatasetAssociationFilter,
)
from core.models.profiles.profile import Profile
from core.models.profiles.profile_version import ProfileVersion
from core.models.profiles.profile_dataset_association import ProfileDatasetAssociation


class BaseProfilesRepository(BaseRepository[Profile, ProfilesWhere, ProfilesFilter]):
    pass


class BaseProfileVersionsRepository(BaseRepository[
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
