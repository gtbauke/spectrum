import pytest

from hypothesis import given, strategies as st, settings, HealthCheck
from iql.compiler import IqlCompiler
from iql.errors.base import AbstractInferenceQueryLanguageError

@pytest.fixture
def compiler():
    return IqlCompiler()

@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], max_examples=50)
@given(st.text())
def test_compiler_never_crashes_on_random_input(compiler, text):
    """
    Property-based test: The compiler should never raise a raw Exception.
    It should either succeed or raise a managed IQL error.
    """
    try:
        compiler.compile(text, available_models=["model_a"])
    except AbstractInferenceQueryLanguageError:
        pass
    except Exception as e:
        # If it reaches here, it's a bug in the compiler (unhandled exception)
        pytest.fail(f"Compiler raised unhandled exception {type(e).__name__}: {e} on input {text!r}")

@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(st.from_regex(r"^SELECT (TOP [0-9]+ )?[a-zA-Z_]+ FROM [a-zA-Z_]+$"))
def test_compiler_handles_valid_looking_garbage(compiler, query):
    # This generates strings that look like IQL but might have random identifiers
    # We just want to ensure it doesn't crash
    compiler.compile(query, available_models=["MODEL_A"])
