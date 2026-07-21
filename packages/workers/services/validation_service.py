import asyncio
import concurrent.futures
import json
import logging
import pandas as pd
import numpy as np
from pathlib import Path
from reggression import Reggression  # type: ignore

from core.features.profiles.models.model import Model

logger = logging.getLogger(__name__)


class ValidationService:
    """Service to evaluate Pareto front expressions against validation datasets."""

    def __init__(self) -> None:
        pass

    def _load_dataset(self, artifact_path: str) -> pd.DataFrame:
        """Loads a CSV dataset from local storage."""
        return pd.read_csv(artifact_path)

    @staticmethod
    def _run_validation(
        model_path: str,
        dataset_path: str,
    ) -> pd.DataFrame:
        """Evaluates Pareto front against validation dataset.

        Returns a DataFrame containing Pareto front expressions and their errors on the validation set.
        """
        reggression = Reggression(
            dataset=dataset_path, loadFrom=model_path)

        # Get Pareto Front
        # In the context of this library, pareto() evaluated on a new dataset
        # will return the expressions with their fitness/RMSE recalculated on the new data.
        pareto_df = reggression.pareto()

        if not isinstance(pareto_df, pd.DataFrame):
            logger.error(
                "Expected pareto() to return a DataFrame, got %s", type(pareto_df))
            raise ValueError("Unexpected output from Reggression.pareto()")

        return pareto_df

    @staticmethod
    def _calculate_predictions(
        dataset_path: str,
        ids: list[int | str],
        expressions: list[str],
        parameters: list[str],
    ) -> pd.DataFrame:
        """Calculates predicted values for each expression on the dataset.

        Returns a DataFrame where each column is the predicted values for an expression,
        identified by its stable Pareto Front ID.
        """
        from core.features.profiles.blocks.inference.prediction_service import PredictionEvaluationService
        
        # Load dataset
        df = pd.read_csv(dataset_path)

        # Identify Target and Features
        # "Target" is the only name the ground truth can have
        if "target" not in df.columns:
            logger.warning(
                "Column 'target' not found in dataset %s. Falling back to last column.",
                dataset_path,
            )
            target_col = df.columns[-1]
        else:
            target_col = "target"

        feature_cols = [c for c in df.columns if c != target_col]
        actual_y = df[target_col].values
        results = {"actual": actual_y}
        
        variables = {}
        for i, col in enumerate(feature_cols):
            val = df[col].values
            variables[f"x{i}"] = val
            variables[col] = val

        prediction_service = PredictionEvaluationService()
        
        for model_id, expr, p_list in zip(ids, expressions, parameters):
            predicted_y = prediction_service.evaluate_expression(expr, variables, p_list)
            results[f"model_{model_id}"] = predicted_y

        return pd.DataFrame(results)

    async def validate(
        self,
        *,
        model: Model,
        model_egraph_path: str,
        validation_artifact_path: str,
    ) -> tuple[pd.DataFrame, dict]:
        """Runs the validation pipeline.

        Returns
        -------
        tuple[pd.DataFrame, dict]
            (Predictions DataFrame, Summary metrics)
        """
        # 1. Recalculate Pareto meta-data on validation set
        loop = asyncio.get_running_loop()
        with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
            pareto_df = await loop.run_in_executor(
                executor,
                self._run_validation,
                model_egraph_path,
                validation_artifact_path,
            )

        logger.info(
            "Validation complete. Pareto front recalculated for model %s on dataset %s",
            model.id,
            validation_artifact_path,
        )

        logger.info("Pareto front summary:\n%s", pareto_df.head())

        # 2. Calculate raw predictions for each expression
        ids = pareto_df["Id"].tolist()
        expressions = pareto_df["Numpy"].tolist()
        parameters = pareto_df["Parameters"].tolist() if "Parameters" in pareto_df.columns else [
            '[]' for _ in expressions
        ]

        with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
            predictions_df = await loop.run_in_executor(
                executor,
                self._calculate_predictions,
                validation_artifact_path,
                ids,
                expressions,
                parameters,
            )

        # 3. Aggregate metrics
        # We store the pareto front summary in the metrics JSON
        metrics = {
            "pareto_front": pareto_df.to_dict(orient="records"),
            "validated_at": pd.Timestamp.now().isoformat(),
        }

        return predictions_df, metrics
