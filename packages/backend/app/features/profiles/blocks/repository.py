from core.repositories.profiles import BaseProfileBlocksRepository
from core.models.profiles.profile_block import ProfileBlock
from core.models.profiles.where import ProfileBlockWhere, ProfileBlockFilter

from app.core.repository import BaseRepositoryImplementation

from ..models import ProfileBlockORM


class ProfileBlocksRepository(BaseProfileBlocksRepository, BaseRepositoryImplementation[
    ProfileBlock,
    ProfileBlockORM,
    ProfileBlockWhere,
    ProfileBlockFilter
]):
    orm_model = ProfileBlockORM
