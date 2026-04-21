import pytest
import pandas as pd
import pathlib

from eggp import EGGP  # type: ignore
from reggression import Reggression  # type: ignore

from iql.compiler import IqlCompiler
from iql.registry.function import create_default_registry


@pytest.fixture(scope="session")
def real_reggression_model(tmp_path_factory):
    """Trains a real but small EGGP model on an example dataset."""
    dataset_path = pathlib.Path(
        "/home/gusta/dev/spectrum/examples/faculty_salary/FacultySalaries_data.csv")
    if not dataset_path.exists():
        pytest.skip(f"Example dataset not found at {dataset_path}")

    # Load data
    df = pd.read_csv(dataset_path)
    X = df.iloc[:, :-1].to_numpy()
    y = df.iloc[:, -1].to_numpy()

    tmp_dir = tmp_path_factory.mktemp("iql_real_models")
    dump_path = tmp_dir / "model.eg"

    estimator = EGGP(
        gen=2,
        nPop=20,
        dumpTo=str(dump_path),
        simplify=True
    )
    estimator.fit(X, y)

    reg = Reggression(dataset=str(dataset_path), loadFrom=str(dump_path))
    return reg


@pytest.fixture
def function_registry():
    return create_default_registry()


@pytest.fixture
def compiler():
    return IqlCompiler()


@pytest.fixture
def regressions(real_reggression_model):
    """Provider fixture for real regression models."""
    return {
        "model_a": real_reggression_model,
        "model_b": real_reggression_model
    }


@pytest.fixture
def mock_regressions(regressions):
    return regressions
