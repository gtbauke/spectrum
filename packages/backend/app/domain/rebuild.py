from app.domain.datasets.dataset import Dataset
from app.domain.datasets.dataset_metadata import DatasetMetadata
from app.domain.models.model import Model
from app.domain.jobs.job import Job


def rebuild_models():
    Dataset.model_rebuild()
    DatasetMetadata.model_rebuild()
    Model.model_rebuild()
    Job.model_rebuild()
