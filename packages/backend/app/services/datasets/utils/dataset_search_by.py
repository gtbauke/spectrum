from uuid import UUID

from app.utils.exactly_one_model import ExactlyOneModel


class DatasetSearchBy(ExactlyOneModel):
    dataset_id: UUID
