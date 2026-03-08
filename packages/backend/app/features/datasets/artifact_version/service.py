from uuid import UUID

from core.models.datasets.where import DatasetArtifactsWhere
from core.ports.unit_of_work import UnitOfWork
from core.services.base import BaseService
from core.models.datasets.dataset_artifact_version import DatasetArtifactVersion

from ..versions.dto.associate_artifacts import AssociateArtifactsDTO
from .results.bulk_create import BulkCreateAssociationResult, AssociationErrorReason, AssociationError


class DatasetArtifactVersionService(BaseService):
    async def create_bulk_association(
        self,
        *,
        uow: UnitOfWork,
        dataset_version_id: UUID,
        data: AssociateArtifactsDTO,
    ) -> BulkCreateAssociationResult:
        associations = [
            DatasetArtifactVersion.new(
                dataset_artifact_id=d.artifact_id,
                artifact_type=d.artifact_type,
                dataset_version_id=dataset_version_id,
            ) for d in data.associations
        ]

        successful_associations: list[DatasetArtifactVersion] = []
        unsuccessful_associations: list[AssociationError] = []

        for association in associations:
            artifact = await uow.dataset_artifacts.get_unique(
                where=DatasetArtifactsWhere(
                    id=association.dataset_artifact_id,
                )
            )

            if not artifact:
                unsuccessful_associations.append(AssociationError(
                    dataset_version_id=dataset_version_id,
                    artifact_id=association.dataset_artifact_id,
                    artifact_type=association.artifact_type,
                    error_reason=AssociationErrorReason.ARTIFACT_DOES_NOT_EXIST,
                ))

                continue

            if artifact.dataset_id != data.dataset_id:
                unsuccessful_associations.append(AssociationError(
                    dataset_version_id=dataset_version_id,
                    artifact_id=association.dataset_artifact_id,
                    artifact_type=association.artifact_type,
                    error_reason=AssociationErrorReason.ARTIFACT_DOES_NOT_BELONG_TO_DATASET,
                ))

                continue

            result = await uow.dataset_artifact_versions.add(association, commit=False)
            successful_associations.append(result)

        return BulkCreateAssociationResult(
            associated=successful_associations,
            errors=unsuccessful_associations,
        )
