from typing import Protocol, Iterable
from core.common.repositories.base.versioned import IVersionedRepository
from core.common.repositories.base.immutable import IImmutableRepository
from .inference_run import InferenceRun
from .inference_result import InferenceResult
from .where import InferenceRunWhere, InferenceRunFilter, InferenceResultWhere, InferenceResultFilter


class IInferenceRunRepository(
    IVersionedRepository[InferenceRun, InferenceRunWhere, InferenceRunFilter], 
    Protocol
):
    """
    Interface for the inference run repository.
    """
    pass


class IInferenceResultRepository(
    IImmutableRepository[InferenceResult, InferenceResultWhere, InferenceResultFilter],
    Protocol
):
    """
    Interface for the inference result repository.
    Supports bulk addition of results from a single run.
    """
    async def add_many(self, entities: Iterable[InferenceResult]) -> None: ...
