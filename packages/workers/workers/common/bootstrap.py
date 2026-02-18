from core.common.config import Settings
from core.common.logging import setup_logging


def bootstrap() -> Settings:
    setup_logging()
    settings = Settings()

    return settings
