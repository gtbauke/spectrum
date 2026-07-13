import numpy as np
import pandas as pd

from .registry import PostProcessorRegistry


@PostProcessorRegistry.register("GROUPED_SOFTMAX")
class GroupedSoftmaxStrategy:
    def transform(self, df: pd.DataFrame, prediction_col: str, config: dict) -> pd.DataFrame:
        result_df = df.copy()

        temp = max(float(config.get("temp", 1.0)), 1e-5)
        group_col = config.get("group_by_column")

        if not group_col or group_col not in result_df.columns:
            raise ValueError(
                f"Group column '{group_col}' is not present in the DataFrame.")

        scaled_predictions = result_df[prediction_col] / temp
        max_scaled_predictions = scaled_predictions.groupby(
            result_df[group_col]).transform('max')
        exp_predictions = np.exp(scaled_predictions - max_scaled_predictions)

        sum_exp_predictions = exp_predictions.groupby(
            result_df[group_col]).transform('sum')
        result_df["final_prediction"] = exp_predictions / sum_exp_predictions

        return result_df
