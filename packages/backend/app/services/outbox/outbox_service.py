from pydantic import BaseModel

from app.services.outbox.utils.create_outbox import CreateOutboxData
from app.services.outbox.utils.outbox_search_by import OutboxSearchBy
from app.services.outbox.utils.update_outbox import UpdateOutboxData

from core.models.outbox.outbox import Outbox
from core.ports.unit_of_work import UnitOfWork
from core.services.base import BaseService


# TODO: implement actual typed service
class OutboxService(BaseService[
    Outbox[BaseModel],
    OutboxSearchBy,
    CreateOutboxData[BaseModel],
    UpdateOutboxData[BaseModel],
]):
    """
    Service for handling outbox messages.
    """

    # TODO: implement get_unique in repository
    # and resolve the where parameter to filter
    # by the property specified in the where parameter
    async def get_unique(
        self,
        *,
        uow: UnitOfWork,
        where: OutboxSearchBy
    ) -> Outbox[BaseModel] | None:
        async with uow:
            return await uow.outbox.get_by_id(id=where.resolve())

    # TODO: implement create method
    # TODO: implement update_unique method
    # TODO: implement delete_unique method
    # TODO: implement get_all method
