from app.core.repository import BaseRepositoryImplementation

from core.repositories.profiles import BaseProfileVersionsRepository
from core.models.profiles.profile_version import ProfileVersion
from core.models.profiles.where import ProfileVersionWhere, ProfileVersionFilter

from ..models import ProfileVersionORM


class ProfileVersionsRepository(BaseProfileVersionsRepository, BaseRepositoryImplementation[
    ProfileVersion,
    ProfileVersionORM,
    ProfileVersionWhere,
    ProfileVersionFilter
]):
    orm_model = ProfileVersionORM
