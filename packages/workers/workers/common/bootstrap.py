from core.common.config import Settings
from core.common.logging import setup_logging

from workers.common.config import settings


def bootstrap() -> Settings:
    setup_logging()

    return settings
