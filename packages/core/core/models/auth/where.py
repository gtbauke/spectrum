from core.utils.where import BaseUniqueWhere


class AuthWhere(BaseUniqueWhere):
    token_hash: str
