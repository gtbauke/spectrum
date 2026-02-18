from uuid import UUID

from core.utils.exactly_one_model import ExactlyOneModel


class DatasetSearchBy(ExactlyOneModel):
    dataset_id: UUID
