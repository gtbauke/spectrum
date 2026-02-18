from typing import Union

from core.tasks.datasets.task import DatasetProcessTask
from core.tasks.training.task import ModelTrainTask

AnyTask = Union[
    DatasetProcessTask,
    ModelTrainTask,
]
