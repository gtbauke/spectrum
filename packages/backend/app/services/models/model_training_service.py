import pandas as pd

from pathlib import Path
from eggp import EGGP  # type: ignore
from app.infra.file_storage import FileStorage


class ModelTrainingService:
    def __init__(self, file_storage: FileStorage):
        self._file_storage = file_storage

    async def train_model(self, file_path: str):
        local_path = await self._file_storage.get_full_path(file_path=file_path)
        data = pd.read_csv(local_path)  # type: ignore

        independent_variables = [
            col for col in data.columns if col != "target"
        ]

        X = data[independent_variables]
        y = data["target"]

        model_path = local_path.replace(".csv", "_model.eggp")
        model_path = Path(model_path)
        model_path.touch(exist_ok=True)

        model = EGGP(dumpTo=str(model_path))
        model.fit(X, y)  # type: ignore

        print(f"Model trained and saved to {model_path}")
