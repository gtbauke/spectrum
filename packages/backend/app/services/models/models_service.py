from uuid import UUID

from app.api.deps import UnitOfWork
from app.domain.models.model import Model
from app.db.models.model import ModelORM


class ModelsService:
    def __init__(self):
        pass

    async def create(
        self,
        uow: UnitOfWork,
        *,
        model_name: str,
        dataset_id: UUID,
        version: int,
    ) -> Model:
        async with uow:
            existing_model = await uow.models.get_by_dataset_id(dataset_id)

            if existing_model:
                return existing_model.to_domain()

            model = Model.create(
                name=model_name,
                dataset_id=dataset_id,
                version=version,
            )

            orm = await uow.models.add(ModelORM.from_domain(model))

        return orm.to_domain()

    async def get_trained_models(
        self,
        uow: UnitOfWork,
    ) -> list[Model]:
        async with uow:
            orms = await uow.models.get_all_trained_models()

        return [orm.to_domain() for orm in orms]

    async def get_non_trained_models(
        self,
        uow: UnitOfWork,
    ) -> list[Model]:
        async with uow:
            orms = await uow.models.get_all_non_trained_models()

        return [orm.to_domain() for orm in orms]
