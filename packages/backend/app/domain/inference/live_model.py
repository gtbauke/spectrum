from reggression import Reggression  # type: ignore

from app.domain.models.model import Model
from app.domain.datasets.dataset import Dataset


class LiveModel:
    def __init__(self, *, model: Model, dataset: Dataset, model_path: str, dataset_path: str):
        self._model = model
        self._dataset = dataset
        self._egg = Reggression(
            dataset=dataset_path,
            loadFrom=model_path,
        )
