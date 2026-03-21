from core.common.repositories.base.mutable import IMutableRepository

from .refresh_token import RefreshToken
from .where import AuthWhere, AuthFilter


class IAuthRepository(IMutableRepository[RefreshToken, AuthWhere, AuthFilter]):
    pass
