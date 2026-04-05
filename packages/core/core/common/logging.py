import sys

from logging.config import dictConfig


def setup_logging():
    formatters = {
        "console": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        }
    }

    try:
        import pythonjsonlogger.jsonlogger  # noqa: F401
        formatters["json"] = {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": (
                "%(levelname)s %(name)s %(message)s "
                "%(asctime)s %(correlation_id)s"
            )
        }
    except ImportError:
        pass

    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": formatters,
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "console"
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["default"]
        }
    })
