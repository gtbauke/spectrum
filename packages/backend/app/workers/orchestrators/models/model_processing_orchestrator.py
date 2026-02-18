import asyncio
import logging

from app.workers.orchestrators.models.model_processing_setup import setup_queues
from app.infra.events.rabbitmq import rabbitmq_manager
from app.core.logging import setup_logging
from app.utils.rebuild import rebuild_models
from app.workers.orchestrators.base import BaseOrchestrator

logger = logging.getLogger(__name__)


class ModelProcessingOrchestrator(BaseOrchestrator):
    async def setup(self) -> None:
        setup_logging()
        rebuild_models()

        await rabbitmq_manager.connect()

    async def run(self):
        try:
            await setup_queues()
        finally:
            await rabbitmq_manager.close()


def run():
    logger.info("Starting ModelProcessingOrchestrator")

    orchestrator = ModelProcessingOrchestrator()
    asyncio.run(orchestrator.execute())


if __name__ == "__main__":
    run()
