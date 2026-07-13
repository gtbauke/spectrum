from typing import Protocol, Type, Dict, Any

import pandas as pd


class PostProcessorStrategy(Protocol):
    def transform(self, df: pd.DataFrame, prediction_col: str, config: Dict[str, Any]) -> pd.DataFrame:
        ...


class PostProcessorRegistry:
    _strategies: Dict[str, Type[PostProcessorStrategy]] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(strategy: Type[PostProcessorStrategy]):
            cls._strategies[name] = strategy
            return strategy

        return decorator

    @classmethod
    def get(cls, name: str) -> PostProcessorStrategy:
        if not name or name.upper() == "NONE":
            return cls._strategies.get("NONE", NoOpStrategy)()

        strategy = cls._strategies.get(name.upper())
        if strategy is None:
            raise ValueError(f"PostProcessor strategy '{name}' not found.")

        return strategy()


@PostProcessorRegistry.register("NONE")
class NoOpStrategy:
    def transform(self, df: pd.DataFrame, prediction_col: str, config: Dict[str, Any]) -> pd.DataFrame:
        df["final_prediction"] = df[prediction_col]
        return df
