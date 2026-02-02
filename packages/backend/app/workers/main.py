import asyncio

from app.workers.setup import setup_queues


async def main():
    await setup_queues()


if __name__ == "__main__":
    asyncio.run(main())
