import asyncio
import json
import logging
import pandas as pd
import numpy as np
from pathlib import Path
from reggression import Reggression  # type: ignore

from core.features.profiles.jobs.job import Job
from core.postprocessing.registry import PostProcessorRegistry
from core.features.profiles.models.model import Model

logger = logging.getLogger(__name__)


class ValidationService:
    """Service to evaluate Pareto front expressions against validation datasets."""

    def __init__(self) -> None:
        pass

    def _load_dataset(self, artifact_path: str, group_by_columns: list[str] | None = None) -> pd.DataFrame:
        """Loads a CSV dataset from local storage."""
        df = pd.read_csv(artifact_path)
        df = df.dropna()  # Drop rows with NaN values

        # Group by columns means I need to strip the group by columns from the dataset before validation. The group by columns are not features for the model.
        if group_by_columns:
            for col in group_by_columns:
                if col in df.columns:
                    df = df.drop(columns=[col])
                else:
                    logger.warning(
                        "Group by column %s not found in dataset", col)

        return df

    def _run_validation(
        self,
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

    def _calculate_predictions(
        self,
        model_path: str,
        dataset_path: str,
        ids: list[int | str],
        expressions: list[str],
        parameters: list[str],
        group_by_columns: list[str] | None = None,
    ) -> pd.DataFrame:
        """Calculates predicted values for each expression on the dataset.

        Returns a DataFrame where each column is the predicted values for an expression,
        identified by its stable Pareto Front ID.
        """
        from core.features.profiles.blocks.inference.prediction_service import PredictionEvaluationService

        # Load dataset using helper to ensure correct absolute path
        df = self._load_dataset(dataset_path, group_by_columns)

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
            predicted_y = prediction_service.evaluate_expression(
                expr, variables, p_list)
            results[f"model_{model_id}"] = predicted_y

        return pd.DataFrame(results)

    async def validate(
        self,
        *,
        model: Model,
        model_egraph_path: str,
        validation_artifact_path: str,
        job: Job,
        group_by_columns: list[str] | None = None,
    ) -> tuple[pd.DataFrame, dict]:
        """Runs the validation pipeline.

        Returns
        -------
        tuple[pd.DataFrame, dict]
            (Predictions DataFrame, Summary metrics)
        """
        # 1. Recalculate Pareto meta-data on validation set
        pareto_df = await asyncio.to_thread(
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

        predictions_df = await asyncio.to_thread(
            self._calculate_predictions,
            model_egraph_path,
            validation_artifact_path,
            ids,
            expressions,
            parameters,
            group_by_columns,
        )

        # TODO: post processing should be configurable
        if job.post_processing_type and job.post_processing_type != "NONE":
            if not job.active_group_by_columns:
                logger.error(
                    "Post-processing strategy '%s' requires active group by columns, but none are set for job %s.",
                    job.post_processing_type, job.id)

                raise ValueError(
                    f"Post-processing strategy '{job.post_processing_type}' requires active group by columns.")

            strategy = PostProcessorRegistry.get(job.post_processing_type)
            model_cols = [
                c for c in predictions_df.columns if c.startswith("model_")]

            for col in model_cols:
                processed = strategy.transform(predictions_df, prediction_col=col, config={
                    "temperature": 1.0,
                    "group_by_column": job.active_group_by_columns[0]
                })

                predictions_df[col] = processed["final_prediction"]
                model_id = col.split("_")[1]

                if str(job.post_processing_type) == "GROUPED_SOFTMAX":
                    eps = 1e-15
                    preds = np.clip(
                        processed["final_prediction"], eps, 1 - eps)
                    targets = predictions_df["actual"]

                    log_loss = - \
                        np.mean(targets * np.log(preds) +
                                (1 - targets) * np.log(1 - preds))
                    pareto_df.loc[pareto_df["Id"] == str(
                        model_id), "Fitness"] = log_loss
                else:
                    mse = np.mean(
                        (processed["actual"] - predictions_df["final_prediction"]) ** 2)
                    pareto_df.loc[pareto_df["Id"] ==
                                  str(model_id), "Fitness"] = mse

        pareto_df = pareto_df.sort_values(
            by="Fitness", ascending=True).reset_index(drop=True)

        # 3. Aggregate metrics
        # We store the pareto front summary in the metrics JSON
        metrics = {
            "pareto_front": pareto_df.to_dict(orient="records"),
            "validated_at": pd.Timestamp.now().isoformat(),
        }

        return predictions_df, metrics
