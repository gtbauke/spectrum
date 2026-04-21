import pytest
from iql.compiler import IqlCompiler

def test_compiler_end_to_end_success():
    compiler = IqlCompiler()
    available_models = ["model_a", "model_b"]
    query = "SELECT TOP 10 expression, fitness FROM model_a WHERE size < 20"
    
    result = compiler.compile(query, available_models)
    
    assert result.is_success
    assert result.plan is not None
    assert not result.errors.has_errors()
    # Check plan properties
    root = result.plan.root
    assert root.columns == ["expression", "fitness"]

def test_compiler_semantic_errors():
    compiler = IqlCompiler()
    available_models = ["model_a"]
    query = "SELECT expression FROM ghost_model"
    
    result = compiler.compile(query, available_models)
    
    assert not result.is_success
    assert result.plan is None
    assert result.errors.has_errors()
    assert "MODELNOTFOUND" in str([type(e).__name__.upper() for e in result.errors.errors])

def test_compiler_syntax_errors():
    compiler = IqlCompiler()
    query = "SELECT FROM model" # Missing columns
    
    result = compiler.compile(query, ["model"])
    
    assert not result.is_success
    assert result.errors.has_errors()
