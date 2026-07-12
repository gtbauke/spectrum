import asyncio
import io
import logging

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from eggp import EGGP

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
        pass

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

    def _load_dataset(self, full_path: str, group_by_columns: list[str] | None = None) -> tuple[np.ndarray, np.ndarray]:
        """Reads a CSV file from disk and splits into X (features) and y (target).

        Convention: all columns except the last are features, the last is the target.
        """
        logger.info("Loading dataset from %s", full_path)
        df = pd.read_csv(full_path)
        df = df.dropna()  # Drop rows with NaN values

        # Group by columns means I need to strip the group by columns from the dataset before training. The group by columns are not features for the model.
        if group_by_columns:
            for col in group_by_columns:
                if col in df.columns:
                    df = df.drop(columns=[col])
                else:
                    logger.warning(
                        "Group by column %s not found in dataset", col)

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
        group_by_columns: list[str] | None = None,
    ) -> TrainingResult:
        """Executes the full training pipeline.

        Parameters
        ----------
        job : Job
            The job configuration with training hyperparameters.
        artifact_path : str
            Absolute local path to the dataset CSV file.
        dump_path : str
            Absolute path where the e-graph dump should be written by eggp.

        Returns
        -------
        TrainingResult
            The results CSV bytes and optional e-graph dump bytes.
        """
        estimator = self._build_estimator(job, dump_path=dump_path)
        X, y = self._load_dataset(
            artifact_path, group_by_columns=group_by_columns)

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
