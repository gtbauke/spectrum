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
    ) -> UUID:
        async with uow:
            model = Model.create(
                name=model_name,
                dataset_id=dataset_id,
                version=version,
            )

            orm = await uow.models.add(ModelORM.from_domain(model))

        return orm.id
