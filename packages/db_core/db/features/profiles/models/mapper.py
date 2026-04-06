from db.common.mappers.base import IMapper
from db.features.profiles.models.model import ModelORM

from core.features.profiles.models.model import Model


class ModelsMapper(IMapper[ModelORM, Model]):
    @staticmethod
    def to_domain(orm: ModelORM) -> Model:
        return Model(
            id=orm.id,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            name=orm.name,
            profile_id=orm.profile_id,
            generated_by=orm.generated_by,
            path=orm.path,
            validation_path=orm.validation_path,
            metrics=orm.metrics,
        )

    @staticmethod
    def to_orm(domain: Model) -> ModelORM:
        return ModelORM(
            id=domain.id,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            name=domain.name,
            profile_id=domain.profile_id,
            generated_by=domain.generated_by,
            path=domain.path,
            validation_path=domain.validation_path,
            metrics=domain.metrics,
        )
