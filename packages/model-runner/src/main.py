import json
import pika

from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel
from pika.exchange_type import ExchangeType
from pika.spec import Basic, BasicProperties
from src.utils.env import ENV
from threading import Thread


def publish_status(channel: BlockingChannel, task_id: str, status: str, progress: int | None = None):
    payload = {
        "task_id": task_id,
        "status": status,
        "progress": str(progress) if progress is not None else ""
    }

    channel.basic_publish(
        exchange=ENV.TASKS_STATUS_EXCHANGE,
        routing_key="",
        body=json.dumps(payload),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )


def on_message(connection: BlockingConnection, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    def process():
        try:
            print(f"Processing task with payload: {body.decode()}")
            # TODO: download dataset from S3
            # TODO: preprocess dataset
            # TODO: create EGGP model and train it
            # TODO: upload trained model to S3
            # TODO: send notification of task completion
            # TODO: handle errors and retries
            # TODO: log task progress and results
            # TODO: implement monitoring and alerting
            # TODO: clean up temporary files

            connection.add_callback_threadsafe(
                lambda: channel.basic_ack(
                    method.delivery_tag)  # type: ignore
            )
        except Exception:
            connection.add_callback_threadsafe(
                lambda: channel.basic_reject(
                    method.delivery_tag, requeue=False)  # type: ignore
            )

    Thread(target=process, daemon=True).start()


def setup(channel: BlockingChannel):
    channel.basic_qos(prefetch_count=1)

    channel.exchange_declare(
        exchange=ENV.TASKS_EXCHANGE,
        exchange_type=ExchangeType.direct,  # type: ignore
        durable=True
    )

    channel.exchange_declare(
        exchange=ENV.TASKS_RETRY_EXCHANGE,
        exchange_type=ExchangeType.direct,  # type: ignore
        durable=True
    )

    channel.exchange_declare(
        exchange=ENV.TASKS_DEAD_LETTER_EXCHANGE,
        exchange_type=ExchangeType.direct,  # type: ignore
        durable=True
    )

    channel.exchange_declare(
        exchange=ENV.TASKS_STATUS_EXCHANGE,
        exchange_type=ExchangeType.fanout,  # type: ignore
        durable=True
    )

    channel.queue_declare(
        queue=ENV.TASKS_QUEUE,
        durable=True,
        arguments={
            "x-dead-letter-exchange": ENV.TASKS_RETRY_EXCHANGE,
            "x-dead-letter-routing-key": ENV.TASKS_RETRY_ROUTING_KEY
        }
    )

    channel.queue_declare(
        queue=ENV.TASKS_RETRY_QUEUE,
        durable=True,
        arguments={
            "x-message-ttl": 300_000,
            "x-dead-letter-exchange": ENV.TASKS_EXCHANGE,
            "x-dead-letter-routing-key": ENV.TASKS_EXCHANGE_ROUTING_KEY
        }
    )

    channel.queue_declare(
        queue=ENV.TASKS_STATUS_QUEUE,
        durable=True,
    )

    channel.queue_declare(
        queue=ENV.TASKS_DEAD_LETTER_QUEUE,
        durable=True
    )

    channel.queue_bind(ENV.TASKS_QUEUE, ENV.TASKS_EXCHANGE,
                       routing_key=ENV.TASKS_EXCHANGE_ROUTING_KEY)

    channel.queue_bind(ENV.TASKS_RETRY_QUEUE, ENV.TASKS_RETRY_EXCHANGE,
                       routing_key=ENV.TASKS_RETRY_ROUTING_KEY)

    channel.queue_bind(ENV.TASKS_DEAD_LETTER_QUEUE, ENV.TASKS_DEAD_LETTER_EXCHANGE,
                       routing_key=ENV.TASKS_DEAD_LETTER_ROUTING_KEY)

    channel.queue_bind(ENV.TASKS_STATUS_QUEUE, ENV.TASKS_STATUS_EXCHANGE)


def main():
    print("Model Runner is starting...")

    parameters = pika.ConnectionParameters(
        host=ENV.RABBITMQ_HOST,
        port=int(ENV.RABBITMQ_PORT),
        virtual_host='/',
        credentials=pika.PlainCredentials(
            ENV.RABBITMQ_USERNAME, ENV.RABBITMQ_PASSWORD),
        heartbeat=600,
        blocked_connection_timeout=300
    )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    setup(channel)

    channel.basic_consume(
        queue=ENV.TASKS_QUEUE,
        on_message_callback=lambda ch, method, properties, body: on_message(
            connection, ch, method, properties, body),
        auto_ack=False
    )

    print("Waiting for tasks. To exit press CTRL+C")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Stopping Model Runner...")
        channel.stop_consuming()
    finally:
        connection.close()
