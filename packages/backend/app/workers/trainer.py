import json
import pika

from pika.spec import Basic, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel

from app.core.config import settings


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=pika.PlainCredentials(
                username=settings.RABBITMQ_USER,
                password=settings.RABBITMQ_PASSWORD
            ),
        )
    )

    channel = connection.channel()

    channel.queue_declare(queue="training_jobs", durable=True)  # type: ignore
    channel.basic_qos(prefetch_count=1)

    def callback(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        payload = json.loads(body)
        job_id = payload.get("job_id")

        try:
            print(f"Training job {job_id} started.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    channel.basic_consume(queue="training_jobs",  # type: ignore
                          on_message_callback=callback)

    channel.start_consuming()


if __name__ == "__main__":
    main()
