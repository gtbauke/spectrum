from loguru import logger

import sys
import watchtower
import uuid
import os


ENV = os.getenv("ENV", "development")


logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>",
    level="INFO"
)

logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    level="INFO"
)

if ENV == "production":
    cloudwatch_handler = watchtower.CloudWatchLogHandler(
        log_group="spectrum-app-logs",
        stream_name=f"spectrum-app-instance-{uuid.uuid4()}"
    )

    logger.add(
        cloudwatch_handler,
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        serialize=True
    )
else:
    logger.info("Running in development mode; skipping CloudWatch logging.")
