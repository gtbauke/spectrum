from __future__ import annotations

from app.domain.datasets.dataset import Dataset
from app.domain.datasets.dataset_metadata import DatasetMetadata
from app.domain.models.model import Model
from app.domain.jobs.job import Job


namespace = {  # type: ignore
    "Dataset": Dataset,
    "DatasetMetadata": DatasetMetadata,
    "Model": Model,
    "Job": Job,
}


def rebuild_models():
    DatasetMetadata.model_rebuild(_types_namespace=namespace)  # type: ignore
    Dataset.model_rebuild(_types_namespace=namespace)  # type: ignore
    Job.model_rebuild(_types_namespace=namespace)  # type: ignore
    Model.model_rebuild(_types_namespace=namespace)  # type: ignore
