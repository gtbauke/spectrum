from aws.sqs import delete_message, receive_messages
from config import Config
from db.models import get_model_from_dataset_id, update_model_status
from events import parse_event
from run_task import run_training_task
from utils import ModelStatus, can_start_model_training


def main():
    while True:
        response = receive_messages(Config.SQS_QUEUE_URL)
        messages = response.get("Messages", [])

        if not messages:
            continue

        msg = messages[0]
        event = parse_event(msg["Body"])  # type: ignore

        model = get_model_from_dataset_id(event.dataset_id)

        if not model or not can_start_model_training(model):
            delete_message(Config.SQS_QUEUE_URL,
                           msg["ReceiptHandle"])  # type: ignore
            continue

        update_model_status(model.id, ModelStatus.QUEUED)

        run_training_task(
            cluster_name=Config.ECS_CLUSTER,
            task_definition=Config.ECS_TASK_DEFINITION,
            container_name=Config.CONTAINER_NAME,
            env={
                "MODEL_ID": model.id,
                "DATASET_ID": event.dataset_id,
                "S3_BUCKET": event.bucket,
                "S3_KEY": event.key,
            }
        )

        delete_message(Config.SQS_QUEUE_URL,
                       msg["ReceiptHandle"])  # type: ignore
