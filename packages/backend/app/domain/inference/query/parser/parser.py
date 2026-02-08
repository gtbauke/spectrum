from app.domain.inference.query.parser.base import QueryParser
from app.domain.inference.query.tokenizer.token import Token, TokenKind
from app.domain.inference.query.parser.parselets.identifier_parselet import IdentifierParselet
from app.domain.inference.query.parser.parselets.select_clause_parselet import SelectClauseParselet
from app.domain.inference.query.parser.parselets.number_parselet import NumberParselet


class InferenceQueryParser(QueryParser):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens)

        self.register_prefix_parselet(
            TokenKind.IDENTIFIER, IdentifierParselet())

        self.register_prefix_parselet(
            TokenKind.NUMBER, NumberParselet())

        self.register_prefix_parselet(
            TokenKind.SELECT, SelectClauseParselet())
