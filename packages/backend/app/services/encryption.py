from argon2 import PasswordHasher
from pydantic import SecretStr


class EncryptionService:
    def hash_password(self, plain_text: str) -> SecretStr:
        ph = PasswordHasher()
        hashed = ph.hash(plain_text)

        return SecretStr(hashed)

    def verify_password(self, plain_text: str, hashed: SecretStr) -> bool:
        ph = PasswordHasher()

        try:
            ph.verify(hashed.get_secret_value(), plain_text)
            return True
        except Exception:
            return False
