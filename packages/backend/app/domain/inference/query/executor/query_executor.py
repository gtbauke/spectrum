import logging

from typing import Any
from reggression import Reggression  # type: ignore

from app.domain.inference.query.parser.base import BaseAstNode
from app.domain.inference.query.parser.ast.base import AstNodeKind
from app.domain.inference.query.parser.ast.select import SelectClauseAstNode
from app.domain.inference.query.executor.errors.root_expression_should_be_select_clause_error import (
    RootExpressionShouldBeSelectClauseError,
)
from app.domain.inference.query.parser.ast.top_n import TopNAstNode
from app.domain.inference.query.parser.ast.number import IntegerLiteralAstNode
from app.domain.inference.query.parser.ast.binary_expression import BinaryExpression


logger = logging.getLogger(__name__)


class QueryExecutor:
    def __init__(self, root_node: BaseAstNode, reggression: Reggression):
        self._root_node = root_node
        self._reggression = reggression

    def _calculate_node_value(self, node: BaseAstNode):
        if isinstance(node, IntegerLiteralAstNode):
            return node.value()

        if isinstance(node, BinaryExpression):
            raise NotImplementedError(
                "Binary expression evaluation is not implemented yet. (Arithmetic operations are not supported yet)")

    def _calculate_top_n(self, top_n_node: TopNAstNode) -> int:
        value = top_n_node.top_n()
        if not value:
            return 1

        n_value = self._calculate_node_value(value)

        if not isinstance(n_value, int):
            raise ValueError("Top N value must be an integer")

        return n_value

    def _execute_top_n_expression(self, select_clause: SelectClauseAstNode) -> Any:
        top_n_expression = select_clause.from_clause().top_n_expression()
        n = self._calculate_top_n(top_n_expression)

        result = self._reggression.top(n=n)  # type: ignore

        logger.info(f"Executed TOP N expression with n={n}, result: {result}")

        return result

    def _execute_pareto_expression(self, select_clause: SelectClauseAstNode) -> Any:
        raise NotImplementedError(
            "Pareto expression execution is not implemented yet.")

    def execute(self) -> Any:
        if not isinstance(self._root_node, SelectClauseAstNode):
            raise RootExpressionShouldBeSelectClauseError()

        from_kind = self._root_node.from_clause().kind

        if from_kind == AstNodeKind.TOP_N_EXPRESSION:
            return self._execute_top_n_expression(self._root_node)

        return self._execute_pareto_expression(self._root_node)
