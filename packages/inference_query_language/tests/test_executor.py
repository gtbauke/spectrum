from iql.compiler import IqlCompiler
from iql.executor.query_executor import QueryExecutor
from iql.utils.result import InferenceResultList


def test_executor_full_pipeline(mock_regressions):
    compiler = IqlCompiler()
    query = "SELECT TOP 2 numpy, fitness FROM model_a"
    available_models = list(mock_regressions.keys())

    comp_result = compiler.compile(query, available_models)
    assert comp_result.is_success
    assert comp_result.plan is not None

    executor = QueryExecutor(comp_result.plan, mock_regressions)
    results = executor.execute()

    assert isinstance(results, InferenceResultList)
    assert len(results.results) == 2
    assert hasattr(results.results[0], "numpy")
    assert hasattr(results.results[0], "fitness")


def test_executor_with_where_filtering(mock_regressions):
    compiler = IqlCompiler()
    query = "SELECT TOP 5 id FROM model_a WHERE size > 10"

    comp_result = compiler.compile(query, list(mock_regressions.keys()))
    assert comp_result.is_success
    assert comp_result.plan is not None

    executor = QueryExecutor(comp_result.plan, mock_regressions)
    executor.execute()

    mock_regg = mock_regressions["model_a"]


def test_executor_with_predict(mock_regressions, monkeypatch):
    import numpy as np

    class MockService:
        def evaluate_expression(self, expr, args, params):
            return np.array([1.0, 2.0, 3.0])

    monkeypatch.setattr(
        "core.features.profiles.blocks.inference.prediction_service.PredictionEvaluationService",
        MockService
    )

    compiler = IqlCompiler()
    query = "SELECT TOP 1 PREDICT(x=1.0) FROM model_a"

    comp_result = compiler.compile(query, list(mock_regressions.keys()))
    assert comp_result.is_success
    assert comp_result.plan is not None

    executor = QueryExecutor(comp_result.plan, mock_regressions)
    results = executor.execute()

    assert len(results.results) == 1
    assert results.results[0].prediction is not None
    assert list(results.results[0].prediction) == [1.0, 2.0, 3.0]
