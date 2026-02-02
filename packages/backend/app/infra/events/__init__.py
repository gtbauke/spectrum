from app.infra.events.datasets.rabbit_mq_datasets_events_publisher import RabbitMQDatasetsEventsPublisher
from app.infra.events.datasets.dataset_events_publisher import DatasetsEventsPublisher
from app.infra.events.rabbitmq import rabbitmq_manager


def get_dataset_events_publisher() -> DatasetsEventsPublisher:
    return RabbitMQDatasetsEventsPublisher(
        connection=rabbitmq_manager.connection,
        channel=rabbitmq_manager.channel,
    )
