from __future__ import annotations
from typing import Optional


class Span:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def merge(self, other: Span) -> Span:
        return Span(min(self.start, other.start), max(self.end, other.end))

    def merge_with_last_non_none(self, *other: Optional[Span]) -> Span:
        result = self

        for span in reversed(other):
            if span is not None:
                result = result.merge(span)

        return result
