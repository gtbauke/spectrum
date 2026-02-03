from aio_pika.abc import AbstractIncomingMessage

# from app.infra.file_storage import get_file_storage
from app.workers.schemas.base import EventEnvelope
from app.workers.schemas.start_model_training_event import StartModelTrainingEvent


async def handle_model_training_message(message: AbstractIncomingMessage):
    # file_storage = get_file_storage()

    async with message.process():
        event_data = EventEnvelope[StartModelTrainingEvent].model_validate_json(
            message.body.decode()
        )

        print("Received model training event:", event_data)
