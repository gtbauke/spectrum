import pytest

from iql.tokenizer.tokenizer import QueryTokenizer
from iql.parser.parser import InferenceQueryParser
from iql.analyzer.analyzer import AnalysisContext, SemanticAnalyzer
from iql.analyzer.errors.semantic import (
    ModelNotFoundError, ColumnNotSelectableError, UnknownFunctionError, InvalidWhereIdentifierError)
from iql.registry.function import create_default_registry


@pytest.fixture
def analysis_context(regressions):
    return AnalysisContext(
        available_model_names=list(regressions.keys()),
        function_registry=create_default_registry()
    )


def test_analyzer_success(analysis_context):
    query = "SELECT expression, fitness FROM model_a WHERE size > 5"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    analyzer = SemanticAnalyzer(analysis_context)
    result = analyzer.analyze(ast)

    assert result.is_valid
    assert result.resolved_model_name == "model_a"
    assert result.symbol_table.resolve("expression") is not None
    assert result.symbol_table.resolve("fitness") is not None


def test_analyzer_model_not_found(analysis_context):
    query = "SELECT id FROM ghost_model"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    analyzer = SemanticAnalyzer(analysis_context)
    result = analyzer.analyze(ast)

    assert not result.is_valid
    assert any(isinstance(e, ModelNotFoundError) for e in result.errors.errors)


def test_analyzer_column_not_selectable(analysis_context):
    query = "SELECT ghost_column FROM model_a"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    analyzer = SemanticAnalyzer(analysis_context)
    result = analyzer.analyze(ast)

    assert not result.is_valid
    assert any(isinstance(e, ColumnNotSelectableError)
               for e in result.errors.errors)


def test_analyzer_invalid_where_identifier(analysis_context):
    # 'expression' is selectable but NOT allowed in WHERE clause (per analyzer.py rules)
    query = "SELECT id FROM model_a WHERE expression = 'x + 1'"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    analyzer = SemanticAnalyzer(analysis_context)
    result = analyzer.analyze(ast)

    assert not result.is_valid
    assert any(isinstance(e, InvalidWhereIdentifierError)
               for e in result.errors.errors)


def test_analyzer_should_return_unknown_function_error_for_unknown_functions(
    analysis_context
):
    query = "SELECT UNKNOWN_FUNC(x=1) FROM model_a"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    analyzer = SemanticAnalyzer(analysis_context)
    result = analyzer.analyze(ast)

    assert not result.is_valid
    assert any(isinstance(e, UnknownFunctionError)
               for e in result.errors.errors)


def test_analyzer_should_return_column_is_not_selectable_error(analysis_context):
    query = "SELECT custom FROM model_a WHERE id > 5"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    analyzer = SemanticAnalyzer(analysis_context)
    result = analyzer.analyze(ast)

    assert not result.is_valid
    assert any(isinstance(e, ColumnNotSelectableError)
               for e in result.errors.errors)
