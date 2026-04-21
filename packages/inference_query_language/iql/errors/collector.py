from __future__ import annotations

import logging

from iql.errors.base import AbstractInferenceQueryLanguageError
from iql.utils.span import Span


logger = logging.getLogger(__name__)


class UnhandledCompilerError(AbstractInferenceQueryLanguageError):
    """Wraps an unexpected exception that lacks a specific IQL error class.

    When this error is raised, it signals that a dedicated exception should
    be created for the underlying failure to improve diagnostics.
    """

    def __init__(self, span: Span, cause: Exception):
        self._cause = cause
        super().__init__(
            span,
            f"Unhandled compiler error: {cause!r}. "
            "Consider creating a specific exception for this failure.",
        )

    @property
    def cause(self) -> Exception:
        return self._cause


class IqlErrorCollector:
    """Accumulates errors across all compiler phases.

    Instead of aborting on the first error, each phase appends its
    diagnostics so the user receives a comprehensive error report.
    """

    def __init__(self) -> None:
        self._errors: list[AbstractInferenceQueryLanguageError] = []

    def add(self, error: AbstractInferenceQueryLanguageError) -> None:
        self._errors.append(error)

    def add_unhandled(self, span: Span, cause: Exception) -> None:
        """Wrap an unexpected exception and add it to the collection."""
        wrapped = UnhandledCompilerError(span, cause)
        logger.warning(
            "Unhandled error wrapped — consider creating a specific exception: %r",
            cause,
        )
        self._errors.append(wrapped)

    @property
    def errors(self) -> list[AbstractInferenceQueryLanguageError]:
        return list(self._errors)

    def has_errors(self) -> bool:
        return len(self._errors) > 0

    def clear(self) -> None:
        self._errors.clear()

    def __len__(self) -> int:
        return len(self._errors)

    def __repr__(self) -> str:
        return f"IqlErrorCollector(count={len(self._errors)})"
