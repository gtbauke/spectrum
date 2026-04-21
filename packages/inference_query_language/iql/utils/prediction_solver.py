import numpy as np
import json
import logging

from typing import Any

logger = logging.getLogger(__name__)


class PredictionEvaluationService:
    """Service to evaluate mathematical expressions sequentially using NumPy."""

    def __init__(self):
        self.base_context = {
            "np": np,
            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,
            "exp": np.exp,
            "log": np.log,
            "sqrt": np.sqrt,
            "abs": np.abs,
            "pow": np.power,
        }

    def evaluate_expression(
        self,
        expression: str,
        variables: dict[str, Any],
        parameters: list[float] | str | None = None
    ) -> np.ndarray:
        """
        Evaluates a string expression against a set of variables and parameters.
        Variables should be a dict where values are lists/arrays of numerical inputs, matching x0, x1, etc.
        Parameters should be a list of floats matching t0, t1, etc.
        """
        eval_context = self.base_context.copy()

        # Add x0, x1, etc.
        for var_name, var_val in variables.items():
            if isinstance(var_val, list):
                eval_context[var_name] = np.array(var_val)
            else:
                eval_context[var_name] = var_val

        grouped_x = [v for k, v in variables.items() if k.startswith("x")]
        if grouped_x:
            eval_context["x"] = np.column_stack(grouped_x)

        p_values = []
        if isinstance(parameters, str):
            try:
                p_values = json.loads(parameters)
            except json.JSONDecodeError:
                logger.warning("Failed to decode parameters: %s", parameters)
        elif parameters is not None:
            p_values = parameters

        if isinstance(p_values, (list, np.ndarray)):
            eval_context["t"] = np.array(p_values)
            for j, p in enumerate(p_values):
                eval_context[f"t{j}"] = p

        python_expr = expression.replace("^", "**")

        try:
            predicted_y = eval(python_expr, {"__builtins__": {}}, eval_context)

            # Use the length of the first variable array to broadcast scalar returns
            n_samples = 1
            if variables:
                first_var = next(iter(variables.values()))
                if hasattr(first_var, "__len__") and not isinstance(first_var, str):
                    n_samples = len(first_var)

            if isinstance(predicted_y, (int, float, np.number)):
                predicted_y = np.full(n_samples, predicted_y, dtype=float)

            predicted_y = np.nan_to_num(
                predicted_y, nan=0.0, posinf=1e9, neginf=-1e9)
            return predicted_y

        except Exception as e:
            logger.warning(
                "Failed to evaluate expression '%s': %s", expression, e)
            n_samples = 1

            if variables:
                first_var = next(iter(variables.values()))

                if hasattr(first_var, "__len__") and not isinstance(first_var, str):
                    n_samples = len(first_var)

            return np.zeros(n_samples)
