from aio_pika import ExchangeType
from aio_pika.abc import AbstractChannel, AbstractExchange

from core.infra.tasks import TaskInfraLookup
from core.tasks.dataset import DATASET_RETRY_DELAYS
from core.tasks.training import TRAINING_RETRY_DELAYS


class WorkersQueueSetupResult:
    def __init__(
        self,
        tasks_exchange: AbstractExchange,
        retry_exchange: AbstractExchange,
        dlx_exchange: AbstractExchange,
    ):
        self.tasks_exchange = tasks_exchange
        self.retry_exchange = retry_exchange
        self.dlx_exchange = dlx_exchange


async def setup_rabbitmq(channel: AbstractChannel) -> WorkersQueueSetupResult:
    tasks_exchange = await channel.declare_exchange(
        TaskInfraLookup.MAIN_EXCHANGE,
        ExchangeType.DIRECT,
        durable=True,
    )

    retry_exchange = await channel.declare_exchange(
        TaskInfraLookup.RETRY_EXCHANGE,
        ExchangeType.DIRECT,
        durable=True,
    )

    dlx_exchange = await channel.declare_exchange(
        TaskInfraLookup.DLX_EXCHANGE,
        ExchangeType.FANOUT,
        durable=True,
    )

    dead_letter_queue = await channel.declare_queue(
        TaskInfraLookup.DLQ_QUEUE,
        durable=True,
    )

    await dead_letter_queue.bind(dlx_exchange)

    result = WorkersQueueSetupResult(
        tasks_exchange=tasks_exchange,
        retry_exchange=retry_exchange,
        dlx_exchange=dlx_exchange,
    )

    return result


async def setup_dataset_processing(channel: AbstractChannel) -> None:
    exchange = await channel.get_exchange(TaskInfraLookup.MAIN_EXCHANGE)
    retry_exchange = await channel.get_exchange(TaskInfraLookup.RETRY_EXCHANGE)

    queue = await channel.declare_queue(
        TaskInfraLookup.DATASET_PROCESSING,
        durable=True,
        arguments={
            "x-dead-letter-exchange": TaskInfraLookup.DLX_EXCHANGE,
        }
    )

    await queue.bind(exchange, routing_key=TaskInfraLookup.DATASET_PROCESSING)

    for attempt, delay in DATASET_RETRY_DELAYS.items():
        retry_queue = await channel.declare_queue(
            f"{TaskInfraLookup.DATASET_PROCESSING_RETRY}.{attempt}",
            durable=True,
            arguments={
                "x-dead-letter-exchange": TaskInfraLookup.MAIN_EXCHANGE,
                "x-message-ttl": delay,
                "x-dead-letter-routing-key": TaskInfraLookup.DATASET_PROCESSING,
            }
        )

        await retry_queue.bind(retry_exchange, routing_key=f"{TaskInfraLookup.DATASET_PROCESSING_RETRY}.{attempt}")


async def setup_model_training(channel: AbstractChannel) -> None:
    exchange = await channel.get_exchange(TaskInfraLookup.MAIN_EXCHANGE)
    retry_exchange = await channel.get_exchange(TaskInfraLookup.RETRY_EXCHANGE)

    queue = await channel.declare_queue(
        TaskInfraLookup.MODEL_TRAINING,
        durable=True,
        arguments={
            "x-dead-letter-exchange": TaskInfraLookup.DLX_EXCHANGE,
        }
    )

    await queue.bind(exchange, routing_key=TaskInfraLookup.MODEL_TRAINING)

    for attempt, delay in TRAINING_RETRY_DELAYS.items():
        retry_queue = await channel.declare_queue(
            f"{TaskInfraLookup.MODEL_TRAINING_RETRY}.{attempt}",
            durable=True,
            arguments={
                "x-dead-letter-exchange": TaskInfraLookup.MAIN_EXCHANGE,
                "x-message-ttl": delay,
                "x-dead-letter-routing-key": TaskInfraLookup.MODEL_TRAINING,
            }
        )

        await retry_queue.bind(retry_exchange, routing_key=f"{TaskInfraLookup.MODEL_TRAINING_RETRY}.{attempt}")


async def setup_all(channel: AbstractChannel) -> None:
    await setup_rabbitmq(channel)
    await setup_dataset_processing(channel)
    await setup_model_training(channel)
