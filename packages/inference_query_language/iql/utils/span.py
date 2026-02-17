from __future__ import annotations


class Span:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def merge(self, other: Span) -> Span:
        return Span(min(self.start, other.start), max(self.end, other.end))
