from typing import Any

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


class RootBase(DeclarativeBase):
    """
    Root base class for all ORM models in the application.
    This class serves as the foundation for both mutable and immutable models, providing common functionality that can be shared across all ORM models.
    """
    __abstract__ = True
    metadata = metadata

    def to_domain(self) -> Any: ...

    @classmethod
    def from_domain(cls, domain_obj: Any) -> Any: ...
