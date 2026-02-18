from reggression import Reggression  # type: ignore

from core.models.models.model import Model
from core.models.datasets.dataset import Dataset


class LiveModel:
    def __init__(self, *, model: Model, dataset: Dataset, model_path: str, dataset_path: str):
        self._model = model
        self._dataset = dataset
        self._egg = Reggression(
            dataset=dataset_path,
            loadFrom=model_path,
        )

    @property
    def reggression(self) -> Reggression:
        return self._egg
