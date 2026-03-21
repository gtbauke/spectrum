from typing import Protocol

from ..base.root import RootBase
from core.features.base import RootDomainModel


class IMapper[
    T_ORM: RootBase,
    T_Domain: RootDomainModel,
](Protocol):
    @staticmethod
    def to_domain(orm: T_ORM) -> T_Domain: ...

    @staticmethod
    def to_orm(domain: T_Domain) -> T_ORM: ...
