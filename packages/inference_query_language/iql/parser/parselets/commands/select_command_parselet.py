from iql.parser.ast.alias_clause import AliasClauseAstNode
from iql.parser.ast.commands.select_command import ModifierNode, SelectCommandAstNode, SelectableNode
from iql.parser.ast.function_call import FunctionCallAstNode
from iql.parser.ast.identifier import IdentifierAstNode
from iql.parser.ast.number import IntegerLiteralAstNode, NumericLiteralAstNode
from iql.parser.ast.pattern_matching_expression import PatternMatchingExpression
from iql.parser.ast.string import StringLiteralAstNode
from iql.parser.ast.top_n import DistributionAstNode, ParetoAstNode, TopNAstNode
from iql.parser.ast.where import WhereAstNode
from iql.parser.base import QueryParser
from iql.parser.parselet import PrefixParselet
from iql.parser.parselets.commands.errors.expression_cannot_be_a_pattern import ExpressionCannotBeAPatternError
from iql.parser.parselets.commands.errors.expression_is_not_numeric import ExpressionIsNotNumericError
from iql.parser.parselets.commands.errors.expression_is_not_selectable import ExpressionIsNotSelectableError
from iql.parser.parselets.commands.errors.missing_columns_error import MissingColumnsError
from iql.tokenizer.token import Token, TokenKind


class SelectCommandParselet(PrefixParselet):
    def __init__(self) -> None:
        super().__init__()

    def _parse_selectable(self, parser: QueryParser) -> SelectableNode:
        expression = parser.parse_expression()

        if isinstance(expression, IdentifierAstNode) \
                or isinstance(expression, FunctionCallAstNode) \
                or isinstance(expression, AliasClauseAstNode):
            return expression

        final_span = self._initial_span.merge(expression.span)
        raise ExpressionIsNotSelectableError(expression.kind, final_span)

    def _parse_modifier(self, parser: QueryParser) -> ModifierNode:
        if parser.matches(TokenKind.TOP):
            value = parser.parse_expression()
            return TopNAstNode(top_n=value, span=self._initial_span.merge(value.span))

        if parser.matches(TokenKind.PARETO):
            return ParetoAstNode(span=self._initial_span)

        if parser.matches(TokenKind.DISTRIBUTION):
            return DistributionAstNode(span=self._initial_span)

        value_10 = IntegerLiteralAstNode(10, self._initial_span)
        return TopNAstNode(top_n=value_10, span=self._initial_span)

    def _parse_where(self, parser: QueryParser, where_token: Token) -> WhereAstNode:
        conditions = parser.do_until_matches(
            TokenKind.PATTERN,
            TokenKind.ORDER,
            TokenKind.AT,
            TokenKind.LIMIT,
            TokenKind.EOF,
            func=lambda p: p.parse_expression(),
        )

        span = where_token.span.merge(
            conditions[-1].span) if conditions else where_token.span

        return WhereAstNode(
            conditions=conditions,
            span=span
        )

    def _parse_pattern(self, parser: QueryParser, pattern_token: Token):
        parser.consume(TokenKind.IS)
        parser.consume(TokenKind.LIKE)

        pattern_expression = parser.parse_expression()
        final_span = pattern_token.span.merge(pattern_expression.span)

        if not isinstance(pattern_expression, StringLiteralAstNode):
            raise ExpressionCannotBeAPatternError(
                pattern_expression.kind, final_span)

        return PatternMatchingExpression(
            pattern=pattern_expression,
            span=final_span,
        )

    def _parse_at_least(self, parser: QueryParser, at_token: Token) -> NumericLiteralAstNode:
        parser.consume(TokenKind.LEAST)
        at_least = parser.parse_expression()

        if not isinstance(at_least, NumericLiteralAstNode):
            span = at_token.span.merge(at_least.span)
            raise ExpressionIsNotNumericError(at_least.kind, span)

        return at_least

    def _parse_limit(self, parser: QueryParser, limit_token: Token) -> IntegerLiteralAstNode:
        limit = parser.parse_expression()

        if not isinstance(limit, IntegerLiteralAstNode):
            span = limit_token.span.merge(limit.span)
            raise ExpressionIsNotNumericError(limit.kind, span)

        return limit

    def parse(self, parser: QueryParser, token: Token) -> SelectCommandAstNode:
        self._initial_span = token.span

        modifier = self._parse_modifier(parser)
        columns = parser.parse_comma_separated_list(self._parse_selectable)
        if not columns:
            raise MissingColumnsError(self._initial_span)

        parser.consume(TokenKind.FROM)
        model_identifier_token = parser.consume(TokenKind.IDENTIFIER)
        model_identifier = IdentifierAstNode(
            model_identifier_token.lexeme, model_identifier_token.span)

        where_token = parser.matches_and_return(TokenKind.WHERE)
        where_clause = self._parse_where(
            parser, where_token) if where_token else None

        pattern_token = parser.matches_and_return(TokenKind.PATTERN)
        pattern_expression = self._parse_pattern(
            parser, pattern_token) if pattern_token else None

        order_by_token = parser.matches_and_return(TokenKind.ORDER)
        if order_by_token:
            raise NotImplementedError("ORDER BY clause is not implemented yet")

        at_least_token = parser.matches_and_return(TokenKind.AT)
        at_least = self._parse_at_least(
            parser, at_least_token) if at_least_token else None

        limit_token = parser.matches_and_return(TokenKind.LIMIT)
        limit = self._parse_limit(parser, limit_token) if limit_token else None

        return SelectCommandAstNode(
            span=self._initial_span,
            columns=columns,
            from_model=model_identifier,
            modifier=modifier,
            where=where_clause,
            pattern_matching_expression=pattern_expression,
            # order_by=None,
            is_distribution=isinstance(modifier, DistributionAstNode),
            at_least=at_least,
            limit=limit,
        )
