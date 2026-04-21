import pytest

from iql.parser.ast.top_n import DistributionAstNode, ParetoAstNode, TopNAstNode
from iql.parser.base import ExpectedTokenException, InfixParseletNotFoundException, PrefixParseletNotFoundException
from iql.parser.parselets.commands.errors.expression_is_not_selectable import ExpressionIsNotSelectableError
from iql.parser.parselets.commands.select_command_parselet import ExpressionCannotBeAPatternError, ExpressionIsNotNumericError, MissingColumnsError
from iql.parser.parselets.errors.base import AbstractParseletError
from iql.parser.parselets.errors.expected_number import ExpectedNumberParseError
from iql.parser.parselets.function_call_parselet import ExpectedIdentifierParseError
from iql.tokenizer.tokenizer import QueryTokenizer
from iql.parser.parser import InferenceQueryParser
from iql.parser.ast.commands.select_command import SelectCommandAstNode
from iql.parser.ast.identifier import IdentifierAstNode
from iql.parser.ast.number import FloatLiteralAstNode, IntegerLiteralAstNode
from iql.parser.ast.binary_expression import BinaryExpression
from iql.parser.ast.function_call import FunctionCallAstNode
from iql.parser.ast.binary_expression import BinaryOperator
from iql.parser.errors.base import QueryParserError


def test_parse_simple_select():
    query = "SELECT expression FROM model"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)

    ast = parser.parse_expression()

    assert isinstance(ast, SelectCommandAstNode)
    assert ast.from_model().name() == "model"
    assert len(ast.columns()) == 1
    assert isinstance(ast.columns()[0], IdentifierAstNode)
    assert ast.columns()[0].name() == "expression"


def test_parse_complex_select():
    query = "SELECT TOP 10 id, expression, fitness FROM model"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    assert isinstance(ast, SelectCommandAstNode)
    assert len(ast.columns()) == 3
    assert ast.modifier() is not None

    modifier = ast.modifier()
    assert modifier is not None
    assert isinstance(modifier, TopNAstNode)

    top_n = modifier.top_n()
    assert top_n is not None
    assert isinstance(top_n, IntegerLiteralAstNode)

    value = top_n.value()
    assert value == 10


def test_parse_select_with_trailing_commas():
    query = "SELECT , id, expression, FROM model"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    assert isinstance(ast, SelectCommandAstNode)
    assert len(ast.columns()) == 2

    assert isinstance(ast.columns()[0], IdentifierAstNode)
    assert ast.columns()[0].name() == "id"

    assert isinstance(ast.columns()[1], IdentifierAstNode)
    assert ast.columns()[1].name() == "expression"


def test_parse_select_with_invalid_semantics():
    query = "SELECT 10, 'string' FROM model"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)

    with pytest.raises(ExpressionIsNotSelectableError):
        parser.parse_expression()


def test_parse_select_with_pareto_modifier():
    query = "SELECT PARETO expression FROM model"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    assert isinstance(ast, SelectCommandAstNode)
    assert ast.modifier() is not None

    modifier = ast.modifier()
    assert modifier is not None
    assert isinstance(modifier, ParetoAstNode)


def test_parse_select_with_distribution_modifier():
    query = "SELECT DISTRIBUTION expression FROM model"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    assert isinstance(ast, SelectCommandAstNode)
    assert ast.modifier() is not None

    modifier = ast.modifier()
    assert modifier is not None
    assert isinstance(modifier, DistributionAstNode)


def test_parse_where_clause():
    query = "SELECT id FROM model WHERE size > 5 AND cost < 10"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    assert isinstance(ast, SelectCommandAstNode)

    where = ast.where()
    assert where is not None

    conditions = where.conditions()
    assert len(conditions) == 1

    expr = conditions[0]
    assert isinstance(expr, BinaryExpression)
    assert expr.operator() == BinaryOperator.AND


def test_parse_function_call():
    query = "SELECT PREDICT(x=1.0, y=2.0) FROM model"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    assert isinstance(ast, SelectCommandAstNode)

    col = ast.columns()[0]
    assert isinstance(col, FunctionCallAstNode)
    assert col.function_name == "PREDICT"
    assert len(col.arguments) == 2
    assert col.arguments[0].variable.name() == "x"


def test_parse_unexpected_token():
    query = "SELECT FROM model"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)

    with pytest.raises(MissingColumnsError):
        parser.parse_expression()


def test_parse_pattern_matching_expression():
    query = "SELECT id, expression FROM model PATTERN IS LIKE 'sin(v0)'"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    assert isinstance(ast, SelectCommandAstNode)
    assert ast.pattern_matching_expression() is not None

    pattern_matching_expression = ast.pattern_matching_expression()
    assert pattern_matching_expression is not None
    assert pattern_matching_expression.pattern.value == "sin(v0)"


def test_parse_pattern_matching_no_is_like():
    query = "SELECT id, expression FROM model PATTERN 'sin(v0)'"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)

    with pytest.raises(ExpectedTokenException):
        parser.parse_expression()


def test_parse_pattern_matching_no_like():
    query = "SELECT id, expression FROM model PATTERN IS 'sin(v0)'"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)

    with pytest.raises(ExpectedTokenException):
        parser.parse_expression()


def test_parse_pattern_not_string():
    query = "SELECT id, expression FROM model PATTERN IS LIKE 123"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)

    with pytest.raises(ExpressionCannotBeAPatternError):
        parser.parse_expression()


def test_parse_at_least():
    query = "SELECT id FROM model AT LEAST 5"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    assert isinstance(ast, SelectCommandAstNode)
    assert ast.at_least() is not None

    at_least = ast.at_least()
    assert at_least is not None
    assert at_least.value() == 5


def test_parse_at_least_non_numeric():
    query = "SELECT id FROM model AT LEAST 'five'"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)

    with pytest.raises(ExpressionIsNotNumericError):
        parser.parse_expression()


def test_parse_at_least_non_integer():
    query = "SELECT id FROM model AT LEAST 5.5"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    assert isinstance(ast, SelectCommandAstNode)
    assert ast.at_least() is not None

    at_least = ast.at_least()
    assert at_least is not None
    assert at_least.value() == 5.5


def test_parse_at_least_no_least():
    query = "SELECT id FROM model AT 5"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)

    with pytest.raises(ExpectedTokenException):
        parser.parse_expression()


def test_parse_at_least_no_number():
    query = "SELECT id FROM model AT LEAST"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)

    with pytest.raises(PrefixParseletNotFoundException):
        parser.parse_expression()


def test_parse_limit():
    query = "SELECT id FROM model LIMIT 10"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    assert isinstance(ast, SelectCommandAstNode)
    assert ast.limit() is not None

    limit = ast.limit()
    assert limit is not None
    assert limit.value() == 10


def test_parse_limit_no_number():
    query = "SELECT id FROM model LIMIT"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)

    with pytest.raises(PrefixParseletNotFoundException):
        parser.parse_expression()


def test_parse_limit_non_integer():
    query = "SELECT id FROM model LIMIT 10.5"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)

    with pytest.raises(ExpressionIsNotNumericError):
        parser.parse_expression()


def test_function_call_name_must_be_identifier():
    query = "SELECT 123(x=1.0) FROM model"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)

    with pytest.raises(ExpectedIdentifierParseError):
        parser.parse_expression()


def test_function_call_is_valid():
    query = "SELECT PREDICT(x=1.0) FROM model"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)

    ast = parser.parse_expression()

    assert isinstance(ast, SelectCommandAstNode)

    col = ast.columns()[0]
    assert isinstance(col, FunctionCallAstNode)
    assert col.function_name == "PREDICT"
    assert col.name() == "predict"
    assert len(col.arguments) == 1
    assert col.arguments[0].variable.name() == "x"
    assert isinstance(col.arguments[0].value, FloatLiteralAstNode)
    assert col.arguments[0].value.value() == 1.0


def test_function_argument_must_be_numeric():
    query = "SELECT PREDICT(x='not a number') FROM model"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)

    with pytest.raises(ExpectedNumberParseError):
        parser.parse_expression()
