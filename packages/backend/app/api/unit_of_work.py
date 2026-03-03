from db.session import AsyncSessionLocal

from app.core.unit_of_work import SqlAlchemyUnitOfWork


async def get_uow():
    async with SqlAlchemyUnitOfWork(session_factory=AsyncSessionLocal) as uow:
        yield uow
