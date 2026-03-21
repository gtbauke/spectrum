from __future__ import annotations

from core.features.users.user import User
from core.features.auth.refresh_token import RefreshToken

namespace = {  # type: ignore
    "User": User,
    "RefreshToken": RefreshToken,
}

for item in [
    User,
    RefreshToken,
]:
    item.model_rebuild(_types_namespace=namespace)
