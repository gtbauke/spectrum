from __future__ import annotations

from core.models.datasets.dataset import Dataset
from core.models.datasets.dataset_metadata import DatasetMetadata
from core.models.models.model import Model
from core.models.jobs.job import Job
from core.models.jobs.job_run import JobRun


namespace = {  # type: ignore
    "Dataset": Dataset,
    "DatasetMetadata": DatasetMetadata,
    "Model": Model,
    "Job": Job,
    "JobRun": JobRun,
}


def rebuild_models():
    DatasetMetadata.model_rebuild(_types_namespace=namespace)  # type: ignore
    Dataset.model_rebuild(_types_namespace=namespace)  # type: ignore
    Job.model_rebuild(_types_namespace=namespace)  # type: ignore
    Model.model_rebuild(_types_namespace=namespace)  # type: ignore
    JobRun.model_rebuild(_types_namespace=namespace)  # type: ignore
