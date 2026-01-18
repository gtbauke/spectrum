import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties


TASKS_QUEUE = 'dataset_training_tasks'


def callback(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    print(f"Received task: {body.decode()}")
    print("Task completed")

    if not method.delivery_tag:
        print("No delivery tag found, cannot acknowledge message.")
        return

    ch.basic_ack(delivery_tag=method.delivery_tag)

    # TODO: download dataset from S3
    # TODO: preprocess dataset
    # TODO: create EGGP model and train it
    # TODO: upload trained model to S3
    # TODO: send notification of task completion
    # TODO: handle errors and retries
    # TODO: log task progress and results
    # TODO: implement monitoring and alerting
    # TODO: clean up temporary files


def main():
    print("Model Runner is starting...")

    # TODO: load configuration from file or environment variables
    parameters = pika.ConnectionParameters(
        host='localhost',
        port=5672,
        virtual_host='/',
        credentials=pika.PlainCredentials('guest', 'guest'),
        heartbeat=60,
        blocked_connection_timeout=300
    )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=TASKS_QUEUE, durable=True)  # type: ignore
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(  # type: ignore
        queue=TASKS_QUEUE, on_message_callback=callback)

    channel.start_consuming()
