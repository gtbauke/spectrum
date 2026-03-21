from fastapi import HTTPException, status

from db.common.session import AsyncSessionLocal
from db.adapters.unit_of_work import SqlAlchemyUnitOfWork

from app.main import state


async def get_uow():
    if not state.message_broker:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Message broker not initialized",
        )

    async with SqlAlchemyUnitOfWork(
        session_factory=AsyncSessionLocal,
        broker=state.message_broker,
    ) as uow:
        yield uow
