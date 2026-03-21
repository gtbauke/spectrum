from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyBaseRepository[T_ORM]:
    """
    Base class for all concrete SQLAlchemy repositories.
    """

    def __init__(self, session: AsyncSession, model_class: Type[T_ORM]) -> None:
        self._session = session
        self._model_class = model_class
