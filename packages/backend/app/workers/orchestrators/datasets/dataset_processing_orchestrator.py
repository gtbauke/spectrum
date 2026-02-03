import asyncio

from app.workers.orchestrators.datasets.dataset_processing_setup import setup_queues
from app.infra.events.rabbitmq import rabbitmq_manager


async def main():
    await rabbitmq_manager.connect()

    try:
        await setup_queues()
    finally:
        await rabbitmq_manager.close()


if __name__ == "__main__":
    asyncio.run(main())
