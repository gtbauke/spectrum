import asyncio
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
    ) -> pd.DataFrame:
        """Calculates predicted values for each expression on the dataset.

        Returns a DataFrame where each column is the predicted values for an expression,
        identified by its stable Pareto Front ID.
        """
        # Load dataset using helper to ensure correct absolute path
        df = self._load_dataset(dataset_path)

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

        # Prepare 2D Feature Matrix 'x' (N x D) for NumPy indexing x[:, i]
        x_matrix = df[feature_cols].values

        # Prepare results container
        results = {"actual": actual_y}

        # Shared evaluation context (math and features)
        base_context = {
            "np": np,
            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,
            "exp": np.exp,
            "log": np.log,
            "sqrt": np.sqrt,
            "abs": np.abs,
            "pow": np.power,
            "x": x_matrix,
        }

        # Add x0, x1... and original feature names as fallbacks
        for i, col in enumerate(feature_cols):
            val = df[col].values
            base_context[f"x{i}"] = val
            base_context[col] = val

        for model_id, expr, p_list in zip(ids, expressions, parameters):
            try:
                # Decode parameters if they are strings (JSON serialized)
                p_values = []
                if isinstance(p_list, str):
                    try:
                        p_values = json.loads(p_list)
                    except json.JSONDecodeError:
                        logger.warning("Failed to decode parameters for model %s: %s", model_id, p_list)
                        p_values = []
                else:
                    p_values = p_list

                # Add parameters 't' to context for this specific model
                eval_context = base_context.copy()
                if isinstance(p_values, (list, np.ndarray)):
                    eval_context["t"] = p_values
                    # Fallback for individual t0, t1...
                    for j, p in enumerate(p_values):
                        eval_context[f"t{j}"] = p

                # Evaluate expression
                python_expr = expr.replace("^", "**")
                predicted_y = eval(
                    python_expr, {"__builtins__": {}}, eval_context)

                # Handle scalar return values (constant models)
                if isinstance(predicted_y, (int, float, np.number)):
                    predicted_y = np.full_like(
                        actual_y, predicted_y, dtype=float)

                # Clean up values (clamping)
                predicted_y = np.nan_to_num(
                    predicted_y, nan=0.0, posinf=1e9, neginf=-1e9)

                # Use stable Model ID as column name
                results[f"model_{model_id}"] = predicted_y
            except Exception as e:
                logger.warning(
                    "Failed to evaluate model %s expression '%s': %s", model_id, expr, e)
                results[f"model_{model_id}"] = np.zeros_like(actual_y)

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
        )

        # 3. Aggregate metrics
        # We store the pareto front summary in the metrics JSON
        metrics = {
            "pareto_front": pareto_df.to_dict(orient="records"),
            "validated_at": pd.Timestamp.now().isoformat(),
        }

        return predictions_df, metrics
