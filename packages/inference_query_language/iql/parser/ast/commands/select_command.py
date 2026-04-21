from typing import Union
from iql.parser.ast.alias_clause import AliasClauseAstNode
from iql.parser.ast.base import BaseAstNode, AstNodeKind
from iql.parser.ast.function_call import FunctionCallAstNode
from iql.parser.ast.identifier import IdentifierAstNode
from iql.parser.ast.number import IntegerLiteralAstNode, NumericLiteralAstNode
from iql.parser.ast.pattern_matching_expression import PatternMatchingExpression
from iql.parser.ast.top_n import DistributionAstNode, ParetoAstNode, TopNAstNode
from iql.parser.ast.where import WhereAstNode
from iql.utils.span import Span


type SelectableNode = Union[
    IdentifierAstNode,
    FunctionCallAstNode,
    AliasClauseAstNode,
]

type ModifierNode = Union[
    TopNAstNode,
    ParetoAstNode,
    DistributionAstNode,
]


class SelectCommandAstNode(BaseAstNode):
    """
    Represents a SELECT command in the AST.

    Attributes:
        columns: A list of columns to select, which can be identifiers, function calls, or alias clauses.
        from_model: The model from which to select data, represented as an identifier.
        modifier: An optional modifier for the SELECT command, such as TOP N or PARETO.
        where: An optional WHERE clause for filtering results.
        order_by: An optional ORDER BY clause for sorting results.
        pattern_matching_expression: An optional pattern matching expression for more complex queries.
        is_distribution: A boolean indicating whether the query is a distribution query.
        at_least: An optional integer specifying a minimum number of results to return.
        limit: An optional integer specifying a maximum number of results to return.
    """

    def __init__(
        self,
        span: Span,
        columns: list[SelectableNode],
        from_model: IdentifierAstNode,
        modifier: ModifierNode | None = None,
        where: WhereAstNode | None = None,
        # order_by: OrderByClauseAstNode | None = None,
        pattern_matching_expression: PatternMatchingExpression | None = None,
        is_distribution: bool = False,
        at_least: NumericLiteralAstNode | None = None,
        limit: IntegerLiteralAstNode | None = None,
    ):
        super().__init__(AstNodeKind.SELECT_CLAUSE, span)
        self._columns = columns
        self._from_model = from_model
        self._modifier = modifier
        self._where = where
        # self._order_by = order_by
        self._pattern_matching_expression = pattern_matching_expression
        self._is_distribution = is_distribution
        self._at_least = at_least
        self._limit = limit

    def columns(self) -> list[SelectableNode]:
        return self._columns

    def from_model(self) -> IdentifierAstNode:
        return self._from_model

    def modifier(self) -> ModifierNode | None:
        return self._modifier

    def where(self) -> WhereAstNode | None:
        return self._where

    # def order_by(self) -> OrderByClauseAstNode | None:
    #     return self._order_by

    def pattern_matching_expression(self) -> PatternMatchingExpression | None:
        return self._pattern_matching_expression

    def is_distribution(self) -> bool:
        return self._is_distribution

    def at_least(self) -> NumericLiteralAstNode | None:
        return self._at_least

    def limit(self) -> IntegerLiteralAstNode | None:
        return self._limit

    def to_string(self, indent: int) -> str:
        indent_str = " " * indent
        modifier_str = f" {self._modifier.to_string(0)}" if self._modifier else ""
        columns_str = ", ".join(column.to_string(0)
                                for column in self._columns)
        from_str = f" FROM {self._from_model.to_string(0)}"
        where_str = f" {self._where.to_string(0)}" if self._where else ""
        # order_by_str = f" {self._order_by.to_string(0)}" if self._order_by else ""
        pattern_matching_str = f" {self._pattern_matching_expression.to_string(0)}" if self._pattern_matching_expression else ""
        distribution_str = " DISTRIBUTION" if self._is_distribution else ""
        at_least_str = f" AT LEAST {self._at_least}" if self._at_least is not None else ""
        limit_str = f" LIMIT {self._limit}" if self._limit is not None else ""

        return f"{indent_str}SELECT{modifier_str} {columns_str}{from_str}{where_str}{pattern_matching_str}{distribution_str}{at_least_str}{limit_str}"
