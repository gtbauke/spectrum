from db.common.mappers.base import IMapper
from db.features.profiles.model import ProfileORM

from core.features.profiles.profile import Profile
from core.features.profiles.profile_mode import ProfileMode

from db.features.datasets.mapper import DatasetsMapper
from db.features.profiles.jobs.mapper import JobsMapper
from db.features.profiles.blocks.mapper import BlockMapper
from db.features.profiles.models.mapper import ModelsMapper


class ProfilesMapper(IMapper[ProfileORM, Profile]):
    @staticmethod
    def to_domain(orm: ProfileORM) -> Profile:
        return Profile(
            id=orm.id,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            deleted_at=orm.deleted_at,
            name=orm.name,
            description=orm.description,
            owner_id=orm.owner_id,
            mode=ProfileMode(orm.mode),
            datasets=[
                DatasetsMapper.to_domain(dataset)
                for dataset in orm.datasets
            ],
            jobs=[
                JobsMapper.to_domain(job)
                for job in orm.jobs
            ],
            blocks=[
                BlockMapper.to_domain(block)
                for block in orm.blocks
            ],
            models=[
                ModelsMapper.to_domain(model)
                for model in orm.models
            ],
        )

    @staticmethod
    def to_orm(domain: Profile) -> ProfileORM:
        return ProfileORM(
            id=domain.id,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            deleted_at=domain.deleted_at,
            name=domain.name,
            description=domain.description,
            owner_id=domain.owner_id,
            mode=domain.mode.value,
            datasets=[
                DatasetsMapper.to_orm(dataset)
                for dataset in domain.datasets
            ],
            jobs=[
                JobsMapper.to_orm(job)
                for job in domain.jobs
            ],
            blocks=[
                BlockMapper.to_orm(block)
                for block in domain.blocks
            ],
            models=[
                ModelsMapper.to_orm(model)
                for model in domain.models
            ],
        )
