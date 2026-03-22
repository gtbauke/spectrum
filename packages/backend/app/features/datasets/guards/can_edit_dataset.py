from fastapi import Depends
from uuid import UUID

from core.ports.unit_of_work import UnitOfWork

from app.api.unit_of_work import get_uow
from app.features.datasets.errors.dataset_not_found import DatasetNotFound
from app.features.auth.errors.forbidden import Forbidden
from app.features.auth.guards.get_current_user import get_current_user

from core.features.datasets.where import DatasetWhere


async def can_edit_dataset(
    dataset_id: UUID,
    current_user_id: UUID = Depends(get_current_user),
    uow: UnitOfWork = Depends(get_uow)
) -> None:
    dataset = await uow.datasets.get_unique(DatasetWhere(id=dataset_id))

    if not dataset:
        raise DatasetNotFound()

    if dataset.owner_id != current_user_id:
        raise Forbidden()
