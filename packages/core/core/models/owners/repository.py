from typing import Protocol

from core.common.repositories.base.immutable import IImmutableRepository

from .owner import Owner
from .where import OwnerWhere, OwnerFilter


class IOwnersRepository(IImmutableRepository[Owner, OwnerWhere, OwnerFilter], Protocol):
    pass
