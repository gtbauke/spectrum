from typing import Union

from core.tasks.dataset import DatasetProcessTask
from core.tasks.training import ModelTrainTask

AnyTask = Union[
    DatasetProcessTask,
    ModelTrainTask,
]
