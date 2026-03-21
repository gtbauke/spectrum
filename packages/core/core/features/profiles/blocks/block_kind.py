from enum import StrEnum
from pydantic import BaseModel


class BlockKind(StrEnum):
    MARKDOWN = "markdown"
    INFERENCE = "inference"


class BaseBlock[T](BaseModel):
    kind: BlockKind
    data: T


class MarkdownBlock(BaseBlock[str]):
    kind: BlockKind = BlockKind.MARKDOWN


class InferenceBlock(BaseBlock[str]):
    kind: BlockKind = BlockKind.INFERENCE
