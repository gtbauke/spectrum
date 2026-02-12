from reggression import Reggression  # type: ignore

from app.domain.inference.query.parser.base import BaseAstNode


class QueryExecutor:
    def __init__(self, root_node: BaseAstNode, reggression: Reggression):
        self._root_node = root_node
        self._reggression = reggression

    def execute(self) -> None:
        raise NotImplementedError("Query execution is not implemented yet.")
