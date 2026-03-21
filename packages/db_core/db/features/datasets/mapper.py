from db.common.mappers.base import IMapper
from db.features.datasets.model import DatasetORM, ArtifactORM

from core.features.datasets.dataset import Dataset
from core.features.datasets.artifact import Artifact


class DatasetsMapper(IMapper[DatasetORM, Dataset]):
    @staticmethod
    def to_domain(orm: DatasetORM) -> Dataset:
        return Dataset(
            id=orm.id,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            deleted_at=orm.deleted_at,
            name=orm.name,
            description=orm.description,
            owner_id=orm.owner_id,
            artifacts=[ArtifactMapper.to_domain(
                artifact) for artifact in orm.artifacts],
        )

    @staticmethod
    def to_orm(domain: Dataset) -> DatasetORM:
        return DatasetORM(
            id=domain.id,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            deleted_at=domain.deleted_at,
            name=domain.name,
            description=domain.description,
            owner_id=domain.owner_id,
            artifacts=[ArtifactMapper.to_orm(
                artifact) for artifact in domain.artifacts],
        )


class ArtifactMapper(IMapper[ArtifactORM, Artifact]):
    @staticmethod
    def to_domain(orm: ArtifactORM) -> Artifact:
        return Artifact(
            id=orm.id,
            timestamp=orm.timestamp,
            dataset_id=orm.dataset_id,
            checksum=orm.checksum,
            size_in_bytes=orm.size_in_bytes,
            path=orm.path,
            role=orm.role,
        )

    @staticmethod
    def to_orm(domain: Artifact) -> ArtifactORM:
        return ArtifactORM(
            id=domain.id,
            timestamp=domain.timestamp,
            dataset_id=domain.dataset_id,
            checksum=domain.checksum,
            size_in_bytes=domain.size_in_bytes,
            path=domain.path,
            role=domain.role,
        )
