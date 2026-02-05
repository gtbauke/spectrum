import sys

from logging.config import dictConfig


def setup_logging():
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": (
                    "%(levelname)s %(name)s %(message)s "
                    "%(asctime)s %(correlation_id)s"
                )
            },
            "console": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
            }
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "json",
                "filters": ["correlation_id"]
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["default"]
        },
        "filters": {
            "correlation_id": {
                "()": "app.api.middlewares.correlation_id_middleware.CorrelationIdFilter"
            }
        }
    })
