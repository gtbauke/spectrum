from enum import StrEnum
from typing import Any, Literal
from pydantic import BaseModel


from app.features.profiles.blocks.inference.domain.inference_result import InferenceResult
from app.features.profiles.blocks.inference.domain.inference_run import InferenceRunStatus
from pydantic import Field
from typing import Optional


class BlockKind(StrEnum):
    MARKDOWN = "markdown"
    INFERENCE = "inference"


class BaseBlock[T](BaseModel):
    data: T
    kind: Any


class MarkdownBlock(BaseBlock[str]):
    kind: Literal[BlockKind.MARKDOWN] = BlockKind.MARKDOWN


class InferenceBlock(BaseBlock[str]):
    kind: Literal[BlockKind.INFERENCE] = BlockKind.INFERENCE
    results: list[InferenceResult] = Field(default_factory=list)
    status: InferenceRunStatus = Field(default=InferenceRunStatus.PENDING)
    execution_time_ms: Optional[int] = None
    error: Optional[str] = None
