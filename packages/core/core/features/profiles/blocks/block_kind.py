from enum import StrEnum


class BlockKind(StrEnum):
    MARKDOWN = "markdown"
    INFERENCE = "inference"


class BaseBlock[T]:
    kind: BlockKind
    data: T


class MarkdownBlock(BaseBlock[str]):
    kind: BlockKind = BlockKind.MARKDOWN


class InferenceBlock(BaseBlock[str]):
    kind: BlockKind = BlockKind.INFERENCE
