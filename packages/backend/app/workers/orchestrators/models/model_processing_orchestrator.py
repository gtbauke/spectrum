import asyncio

from app.workers.orchestrators.models.model_processing_setup import setup_queues
from app.infra.events.rabbitmq import rabbitmq_manager


async def main():
    await rabbitmq_manager.connect()

    try:
        await setup_queues()
    finally:
        await rabbitmq_manager.close()


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
