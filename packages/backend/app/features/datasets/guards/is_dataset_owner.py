from fastapi import Depends
from uuid import UUID

from core.ports.unit_of_work import UnitOfWork
from core.models.datasets.where import DatasetsWhere

from app.api.unit_of_work import get_uow
from app.features.auth.errors.forbidden import Forbidden
from app.features.auth.guards.get_current_user import get_current_owner

from ..errors.dataset_not_found import DatasetNotFound


async def is_dataset_owner(
    dataset_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
    current_owner: UUID = Depends(get_current_owner),
):
    dataset = await uow.datasets.get_unique(where=DatasetsWhere(id=dataset_id))

    if not dataset:
        raise DatasetNotFound(dataset_id=dataset_id)

    if dataset.owner_id != current_owner:
        raise Forbidden()

    return dataset
