import asyncio
import io
import logging

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from eggp import EGGP

from core.common.config import Settings
from core.features.profiles.jobs.job import Job

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TrainingResult:
    """Holds the output of a training session."""

    results_csv: bytes
    egraph_dump: bytes | None


class TrainingService:
    """Encapsulates eggp symbolic regression training.

    Operates on domain objects and plain data, with no database dependency.
    """

    def __init__(self) -> None:
        settings = Settings()

        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent

        self._base_path = (project_root /
                           settings.FILE_STORAGE_SPECTRUM_DATA_PATH).resolve()

    def _build_estimator(self, job: Job, *, dump_path: str) -> EGGP:
        """Maps Job domain fields to EGGP constructor parameters."""
        nonterminals_str = ",".join(nt.value for nt in job.non_terminals)

        return EGGP(
            gen=job.generations,
            nPop=job.population,
            maxSize=job.max_size,
            nTournament=job.number_of_tournaments,
            pc=job.crossover_probability,
            pm=job.mutation_probability,
            nonterminals=nonterminals_str,
            loss=job.loss.value,
            optIter=job.optimization_iterations,
            optRepeat=job.optimization_repeats,
            nParams=job.max_param_count,
            folds=job.split,
            simplify=job.simplify,
            dumpTo=dump_path,
        )

    def _load_dataset(self, artifact_path: str) -> tuple[np.ndarray, np.ndarray]:
        """Reads a CSV file from disk and splits into X (features) and y (target).

        Convention: all columns except the last are features, the last is the target.
        """
        full_path = self._base_path / artifact_path.lstrip("/")

        logger.info("Loading dataset from %s", full_path)
        df = pd.read_csv(full_path)

        X = df.iloc[:, :-1].to_numpy()
        y = df.iloc[:, -1].to_numpy()

        logger.info(
            "Dataset loaded: %d rows, %d features",
            X.shape[0],
            X.shape[1],
        )

        return X, y

    def _run_training(
        self,
        estimator: EGGP,
        X: np.ndarray,
        y: np.ndarray,
    ) -> pd.DataFrame:
        """Runs EGGP.fit() synchronously (CPU-bound, Haskell FFI)."""
        estimator.fit(X, y)
        return estimator.results

    async def train(
        self,
        *,
        job: Job,
        artifact_path: str,
        dump_path: str,
    ) -> TrainingResult:
        """Executes the full training pipeline.

        Parameters
        ----------
        job : Job
            The job configuration with training hyperparameters.
        artifact_path : str
            Relative path to the dataset CSV within file storage.
        dump_path : str
            Absolute path where the e-graph dump should be written by eggp.

        Returns
        -------
        TrainingResult
            The results CSV bytes and optional e-graph dump bytes.
        """
        estimator = self._build_estimator(job, dump_path=dump_path)
        X, y = self._load_dataset(artifact_path)

        logger.info(
            "Starting eggp training: gen=%d, pop=%d, max_size=%d",
            job.generations,
            job.population,
            job.max_size,
        )

        results_df = await asyncio.to_thread(self._run_training, estimator, X, y)

        logger.info(
            "Training complete: %d models found",
            len(results_df),
        )

        results_buf = io.BytesIO()
        results_df.to_csv(results_buf, index=False)
        results_csv = results_buf.getvalue()

        egraph_dump: bytes | None = None
        dump_file = Path(dump_path)

        if dump_file.exists():
            egraph_dump = dump_file.read_bytes()

        return TrainingResult(
            results_csv=results_csv,
            egraph_dump=egraph_dump,
        )
