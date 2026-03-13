import logging

from app.core.repository import BaseRepositoryImplementation

from ..models import ProfileDatasetAssociationORM

from core.models.profiles.where import ProfileDatasetAssociationWhere, ProfileDatasetAssociationFilter
from core.models.profiles.profile_dataset_association import ProfileDatasetAssociation
from core.repositories.profiles import BaseProfileDatasetAssociationsRepository


logger = logging.getLogger(__name__)


class ProfileDatasetAssociationsRepository(BaseProfileDatasetAssociationsRepository, BaseRepositoryImplementation[
    ProfileDatasetAssociation,
    ProfileDatasetAssociationORM,
    ProfileDatasetAssociationWhere,
    ProfileDatasetAssociationFilter
]):
    orm_model = ProfileDatasetAssociationORM
