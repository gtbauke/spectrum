import sys
import logging
import asyncio

from workers.common.bootstrap import bootstrap

logger = logging.getLogger(__name__)


def main():
    worker_type = sys.argv[1] if len(sys.argv) > 1 else None

    if not worker_type:
        print("Please specify a worker type (e.g., 'dataset', 'training')")
        exit(1)

    bootstrap()
    logger.info(f"Starting worker of type: {worker_type}")

    if worker_type == "outbox_worker":
        from workers.consumers.outbox_events.publish_outbox_events import publish_outbox_events
        asyncio.run(publish_outbox_events())


if __name__ == "__main__":
    main()
