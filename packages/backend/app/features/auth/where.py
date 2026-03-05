from core.utils.where import BaseWhere


class AuthWhere(BaseWhere):
    token_hash: str
