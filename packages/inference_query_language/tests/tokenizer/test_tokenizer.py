import pytest

from iql.tokenizer.tokenizer import QueryTokenizer
from iql.tokenizer.token import TokenKind
from iql.tokenizer.errors.unterminated_string_error import UnterminatedStringError


def test_tokenize_basic_select():
    query = "SELECT expression FROM model"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()

    assert len(tokens) == 5
    assert tokens[0].kind == TokenKind.SELECT
    assert tokens[1].kind == TokenKind.IDENTIFIER
    assert tokens[2].kind == TokenKind.FROM
    assert tokens[3].kind == TokenKind.IDENTIFIER
    assert tokens[3].lexeme == "MODEL"
    assert tokens[4].kind == TokenKind.EOF


def test_tokenize_numbers():
    query = "123 45.67"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()

    assert tokens[0].kind == TokenKind.NUMBER
    assert tokens[0].lexeme == "123"
    assert tokens[1].kind == TokenKind.NUMBER
    assert tokens[1].lexeme == "45.67"


def test_tokenize_quoted_identifier():
    query = 'SELECT expression FROM "My Model"'
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()

    assert tokens[3].kind == TokenKind.IDENTIFIER
    assert tokens[3].lexeme == "My Model"


def test_tokenize_string_literal():
    query = "WHERE pattern = 'x + 1'"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()

    assert tokens[3].kind == TokenKind.STRING
    assert tokens[3].lexeme == "x + 1"


def test_tokenize_where_clause_with_operators():
    query = "WHERE x > 10 AND y >= 20 OR z <= 5"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()

    assert tokens[0].kind == TokenKind.WHERE
    assert tokens[1].kind == TokenKind.IDENTIFIER
    assert tokens[2].kind == TokenKind.GREATER
    assert tokens[3].kind == TokenKind.NUMBER
    assert tokens[4].kind == TokenKind.AND
    assert tokens[5].kind == TokenKind.IDENTIFIER
    assert tokens[6].kind == TokenKind.GREATER_EQUAL
    assert tokens[7].kind == TokenKind.NUMBER
    assert tokens[8].kind == TokenKind.OR
    assert tokens[9].kind == TokenKind.IDENTIFIER
    assert tokens[10].kind == TokenKind.LESS_EQUAL
    assert tokens[11].kind == TokenKind.NUMBER


def test_tokenizer_arithmetic_operators():
    query = "SELECT x + y - z * 2 / 4"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()

    assert tokens[0].kind == TokenKind.SELECT
    assert tokens[1].kind == TokenKind.IDENTIFIER
    assert tokens[2].kind == TokenKind.PLUS
    assert tokens[3].kind == TokenKind.IDENTIFIER
    assert tokens[4].kind == TokenKind.MINUS
    assert tokens[5].kind == TokenKind.IDENTIFIER
    assert tokens[6].kind == TokenKind.STAR
    assert tokens[7].kind == TokenKind.NUMBER
    assert tokens[8].kind == TokenKind.SLASH
    assert tokens[9].kind == TokenKind.NUMBER


def test_tokenizer_unterminated_quoted_identifier():
    query = 'SELECT expression FROM "unclosed'
    tokenizer = QueryTokenizer(query)

    with pytest.raises(UnterminatedStringError):
        tokenizer.tokenize()


def test_tokenizer_unterminated_string_literal():
    query = "WHERE x = 'unclosed"
    tokenizer = QueryTokenizer(query)

    with pytest.raises(UnterminatedStringError):
        tokenizer.tokenize()


def test_tokenizer_skips_comments():
    query = """
    -- This is a comment
    SELECT expression /* Multi-line
    comment */ FROM model
    """
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()

    assert tokens[0].kind == TokenKind.SELECT
    assert tokens[1].kind == TokenKind.IDENTIFIER
    assert tokens[2].kind == TokenKind.FROM
    assert tokens[3].kind == TokenKind.IDENTIFIER


def test_tokenizer_tokenize_all_keywords():
    keywords = [
        "SELECT",
        "FROM",
        "TOP",
        "WHERE",
        "NOT",
        "AND",
        "OR",
        "ORDER",
        "BY",
        "PARETO",
        "PATTERN",
        "LIKE",
        "IS",
        "DISTRIBUTION",
        "AT",
        "LEAST",
        "LIMIT",
        "INSERT",
        "PLOT",
    ]

    query = " ".join(keywords) + " model"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()

    assert len(tokens) == len(keywords) + 2
    for i, keyword in enumerate(keywords):
        assert tokens[i].kind.name == keyword

    assert tokens[-2].kind == TokenKind.IDENTIFIER
