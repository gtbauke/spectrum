from app.domain.models.model import Model
from app.domain.inference.live_model import LiveModel

from iql.tokenizer.tokenizer import QueryTokenizer
from iql.parser.parser import InferenceQueryParser
from iql.executor.query_executor import QueryExecutor


class InferenceSession:
    def __init__(self, model: Model, live_model: LiveModel):
        self._model = model
        self._live_model = live_model

    async def handle_unsafe_code_execution(self, code: str):
        result = eval(code)
        return result

    async def execute_query(self, query: str):
        tokenizer = QueryTokenizer(query)
        tokens = tokenizer.tokenize()

        parser = InferenceQueryParser(tokens)
        root_node = parser.parse_expression()

        executor = QueryExecutor(root_node, self._live_model.reggression)
        result = executor.execute()

        return result
