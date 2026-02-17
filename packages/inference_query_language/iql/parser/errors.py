from iql.tokenizer.token import TokenKind


class ExpectedTokenException(Exception):
    def __init__(self, expected_kind: TokenKind, actual_token: TokenKind):
        self._expected_kind = expected_kind
        self._actual_token = actual_token

        super().__init__(
            f"Expected token of kind {expected_kind}, but got {actual_token}"
        )
