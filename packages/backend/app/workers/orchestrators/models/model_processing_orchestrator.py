import asyncio

from app.workers.orchestrators.models.model_processing_setup import setup_queues
from app.infra.events.rabbitmq import rabbitmq_manager
from app.core.logging import setup_logging
from app.domain.rebuild import rebuild_models
from app.workers.orchestrators.base import BaseOrchestrator


class ModelProcessingOrchestrator(BaseOrchestrator):
    async def setup(self):
        setup_logging()
        rebuild_models()

        await rabbitmq_manager.connect()

    async def run(self):
        try:
            await setup_queues()
        finally:
            await rabbitmq_manager.close()


def run():
    orchestrator = ModelProcessingOrchestrator()

    asyncio.run(orchestrator.setup())
    asyncio.run(orchestrator.run())


if __name__ == "__main__":
    run()
