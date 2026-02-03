from app.infra.events.datasets.rabbit_mq_datasets_events_publisher import RabbitMQDatasetsEventsPublisher
from app.infra.events.datasets.dataset_events_publisher import DatasetsEventsPublisher
from app.infra.events.models.rabbit_mq_model_events_publisher import RabbitMQModelEventsPublisher
from app.infra.events.models.model_events_publisher import ModelEventsPublisher
from app.infra.events.rabbitmq import rabbitmq_manager


def get_dataset_events_publisher() -> DatasetsEventsPublisher:
    return RabbitMQDatasetsEventsPublisher(
        connection=rabbitmq_manager.connection,
        channel=rabbitmq_manager.channel,
    )


def get_model_events_publisher() -> ModelEventsPublisher:
    return RabbitMQModelEventsPublisher(
        connection=rabbitmq_manager.connection,
        channel=rabbitmq_manager.channel,
    )
